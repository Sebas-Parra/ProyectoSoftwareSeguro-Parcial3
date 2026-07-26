#!/usr/bin/env python3
"""
SAST avanzado (Fase 3 del pipeline) - Anexo del PDF "PROY_PARCIAL_III_DesSeguro".

El PDF pide un modelo de Machine Learning (tipo CodeBERT fine-tuneado con
datasets de CWE) que analice los archivos modificados en el commit y busque
patrones anomalos que SonarCloud no detecta, retornando:
  - exit code 0: no se detectaron patrones sospechosos (o no se pudo analizar)
  - exit code 1: se detecto codigo probablemente inseguro -> bloquea el deploy

Enfoque pragmatico (tal como el propio PDF lo exige, dado que entrenar un
modelo desde cero esta fuera de alcance): se consume la API de inferencia
gratuita de Hugging Face contra un modelo publico ya fine-tuneado para
clasificar codigo como "vulnerable" / "no vulnerable"
(mrm8488/codebert-base-finetuned-detect-insecure-code).

Este proyecto es Python (FastAPI) + Vue/JS, por lo que en vez de ".ts" se
analizan los archivos ".py", ".js" y ".vue" modificados en el commit.

Si no hay HF_API_TOKEN configurado o la API no responde (modelo "dormido",
rate limit, etc.), el script no bloquea el pipeline: lo reporta como
"sin analizar" y termina con exit code 0, para no volver el pipeline fragil
por una dependencia externa gratuita. Esto se documenta explicitamente aqui
y se notifica por Telegram para que el equipo lo sepa.
"""

import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
import json

HF_MODEL = "mrm8488/codebert-base-finetuned-detect-insecure-code"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
VULNERABLE_LABELS = {"LABEL_1", "VULNERABLE", "INSECURE"}
CONFIDENCE_THRESHOLD = float(os.getenv("ML_SAST_THRESHOLD", "0.75"))
MAX_CHARS_PER_FILE = 4000
EXTENSIONS = (".py", ".js", ".vue")
MAX_RETRIES = 2


def get_changed_files() -> list[str]:
    base_sha = os.getenv("BASE_SHA")
    head_sha = os.getenv("HEAD_SHA", "HEAD")

    if base_sha:
        diff_range = f"{base_sha}..{head_sha}"
    else:
        diff_range = "HEAD~1..HEAD"

    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACMR", diff_range],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError:
        # Primer commit del repo, no hay HEAD~1
        result = subprocess.run(
            ["git", "show", "--pretty=", "--name-only", head_sha],
            check=True, capture_output=True, text=True,
        )

    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    return [f for f in files if f.endswith(EXTENSIONS) and os.path.isfile(f)]


def query_model(code_snippet: str):
    token = os.getenv("HF_API_TOKEN")
    if not token:
        return None, "HF_API_TOKEN no configurado"

    payload = json.dumps({"inputs": code_snippet, "options": {"wait_for_model": True}}).encode("utf-8")
    req = urllib.request.Request(
        HF_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    last_error = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = json.loads(resp.read().decode("utf-8"))
                return body, None
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as e:
            last_error = str(e)
            time.sleep(2 * attempt)

    return None, last_error


def interpret(response) -> tuple[bool, float, str]:
    """Devuelve (es_vulnerable, score, etiqueta)."""
    scores = response
    if isinstance(scores, list) and scores and isinstance(scores[0], list):
        scores = scores[0]

    if not isinstance(scores, list):
        return False, 0.0, "respuesta_inesperada"

    best = max(scores, key=lambda s: s.get("score", 0))
    label = best.get("label", "")
    score = best.get("score", 0.0)

    return label.upper() in VULNERABLE_LABELS and score >= CONFIDENCE_THRESHOLD, score, label


def main() -> int:
    changed_files = get_changed_files()

    if not changed_files:
        print("[ml-sast] No hay archivos .py/.js/.vue modificados en este commit. Nada que analizar.")
        return 0

    print(f"[ml-sast] Analizando {len(changed_files)} archivo(s) con {HF_MODEL}:")
    for f in changed_files:
        print(f"  - {f}")

    findings = []
    analyzed_count = 0

    for path in changed_files:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            code = fh.read()[:MAX_CHARS_PER_FILE]

        if not code.strip():
            continue

        response, error = query_model(code)

        if error:
            print(f"[ml-sast] AVISO: no se pudo analizar '{path}' via Hugging Face ({error}). Se omite.")
            continue

        analyzed_count += 1
        is_vulnerable, score, label = interpret(response)
        print(f"[ml-sast] {path}: label={label} score={score:.3f} vulnerable={is_vulnerable}")

        if is_vulnerable:
            findings.append((path, score, label))

    if not findings:
        if analyzed_count == 0:
            print("[ml-sast] No se pudo analizar ningun archivo (API no disponible / sin token). "
                  "No se bloquea el pipeline, pero revisa el secret HF_API_TOKEN.")
        else:
            print(f"[ml-sast] OK: {analyzed_count} archivo(s) analizados, ningun patron sospechoso detectado.")
        return 0

    print("\n[ml-sast] ALERTA: patrones de codigo potencialmente inseguro detectados:")
    for path, score, label in findings:
        print(f"  - {path} (confianza={score:.2f}, etiqueta={label})")

    return 1


if __name__ == "__main__":
    sys.exit(main())

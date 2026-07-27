#!/usr/bin/env python3
"""
Dispara un deploy en Render via su API REST y espera a que termine,
reportando exito (exit 0) o fallo (exit 1). Se usa en la Fase 4 del
pipeline para que el despliegue este realmente triggered por el CI
(no por el webhook automatico de Render en cada push -> Auto-Deploy
debe estar desactivado en cada servicio) y para poder notificar a
Telegram el resultado real, no solo que "se disparo".

Uso: python render_deploy.py <service_id>
Requiere la variable de entorno RENDER_API_KEY.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

API_BASE = "https://api.render.com/v1"
TERMINAL_STATES = {"live", "build_failed", "update_failed", "canceled", "deactivated"}
POLL_INTERVAL_SECONDS = 10
TIMEOUT_SECONDS = 600


def _api_request(api_key: str, method: str, path: str):
    req = urllib.request.Request(
        f"{API_BASE}{path}",
        method=method,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main() -> int:
    if len(sys.argv) != 2:
        print("Uso: python render_deploy.py <service_id>")
        return 1

    service_id = sys.argv[1]
    api_key = os.environ.get("RENDER_API_KEY")

    if not api_key:
        print("[render-deploy] Falta el secret RENDER_API_KEY.")
        return 1
    if not service_id:
        print("[render-deploy] Falta el service_id (revisa el secret correspondiente).")
        return 1

    print(f"[render-deploy] Disparando deploy para {service_id}...")
    try:
        deploy = _api_request(api_key, "POST", f"/services/{service_id}/deploys")
    except urllib.error.HTTPError as e:
        print(f"[render-deploy] Error al crear el deploy: {e.code} {e.read().decode()}")
        return 1

    deploy_id = deploy["id"]
    print(f"[render-deploy] Deploy creado: {deploy_id}")

    elapsed = 0
    while elapsed < TIMEOUT_SECONDS:
        status_response = _api_request(api_key, "GET", f"/services/{service_id}/deploys/{deploy_id}")
        status = status_response.get("status")
        print(f"[render-deploy] Estado: {status} ({elapsed}s transcurridos)")

        if status in TERMINAL_STATES:
            if status == "live":
                print(f"[render-deploy] {service_id}: despliegue exitoso.")
                return 0
            print(f"[render-deploy] {service_id}: fallo con estado '{status}'.")
            return 1

        time.sleep(POLL_INTERVAL_SECONDS)
        elapsed += POLL_INTERVAL_SECONDS

    print(f"[render-deploy] {service_id}: tiempo de espera agotado ({TIMEOUT_SECONDS}s).")
    return 1


if __name__ == "__main__":
    sys.exit(main())

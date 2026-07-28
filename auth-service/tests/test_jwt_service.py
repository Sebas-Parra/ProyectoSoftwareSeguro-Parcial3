import asyncio
import time

import jwt as pyjwt

from services import jwt_service


def run(coro):
    return asyncio.run(coro)


def test_load_key_reads_from_file_path():
    import os
    key = jwt_service._load_key(os.getenv("PRIVATE_KEY"))
    assert key.strip().startswith("-----BEGIN")


def test_load_key_accepts_raw_pem_content_directly():
    """En Railway (sin filesystem compartido entre servicios) la variable
    de entorno lleva el contenido PEM completo, no una ruta a archivo."""
    raw_pem = jwt_service.PUBLIC_KEY  # ya sabemos que es un PEM valido
    loaded = jwt_service._load_key(raw_pem)
    assert loaded == raw_pem.replace("\\n", "\n")


def test_load_key_fixes_escaped_newlines_in_raw_content():
    fake_pem_with_escaped_newlines = "-----BEGIN PUBLIC KEY-----\\nABC123\\n-----END PUBLIC KEY-----\\n"
    loaded = jwt_service._load_key(fake_pem_with_escaped_newlines)
    assert "\\n" not in loaded
    assert "\n" in loaded


def test_temptoken_roundtrip():
    token = run(jwt_service.generar_temptoken(1, "administrador"))
    payload, error = run(jwt_service.verificar_token(token, "access"))

    assert error is None
    assert payload["sub"] == "1"
    assert payload["username"] == "administrador"
    assert payload["type"] == "access"


def test_generar_tokens_embeds_selected_role():
    access_token, refresh_token = run(
        jwt_service.generar_tokens(1, "administrador", "administrador", role_id=1)
    )

    access_payload, error = run(jwt_service.verificar_token(access_token, "access"))
    assert error is None
    assert access_payload["role_id"] == 1


def test_generar_tokens_embeds_modules_for_authorization():
    access_token, refresh_token = run(
        jwt_service.generar_tokens(1, "vendedor", "vendedor", role_id=2, modules=["Ventas"])
    )

    access_payload, _ = run(jwt_service.verificar_token(access_token, "access"))
    refresh_payload, _ = run(jwt_service.verificar_token(refresh_token, "refresh"))

    assert access_payload["modules"] == ["Ventas"]
    assert refresh_payload["modules"] == ["Ventas"]


def test_generar_tokens_defaults_modules_to_empty_list():
    access_token, _ = run(jwt_service.generar_tokens(1, "administrador", "administrador", role_id=1))

    access_payload, _ = run(jwt_service.verificar_token(access_token, "access"))
    assert access_payload["modules"] == []


def test_validar_refresh_token_preserves_modules():
    _, refresh_token = run(
        jwt_service.generar_tokens(1, "vendedor", "vendedor", role_id=2, modules=["Ventas"])
    )

    (new_access, _), error = run(jwt_service.validar_refresh_token(refresh_token))
    assert error is None

    new_payload, _ = run(jwt_service.verificar_token(new_access, "access"))
    assert new_payload["modules"] == ["Ventas"]


def test_verificar_token_rejects_mismatched_type():
    access_token, _ = run(jwt_service.generar_tokens(1, "administrador", "administrador", role_id=1))

    payload, error = run(jwt_service.verificar_token(access_token, "refresh"))

    assert payload is None
    assert error == "Tipo de token incorrecto"


def test_verificar_token_rejects_expired_token():
    now = int(time.time())
    expired_payload = {
        "sub": "1",
        "username": "administrador",
        "type": "access",
        "exp": now - 60,
        "iat": now - 120,
    }
    expired_token = pyjwt.encode(expired_payload, jwt_service.PRIVATE_KEY, algorithm=jwt_service.ALGORITHM)

    payload, error = run(jwt_service.verificar_token(expired_token, "access"))

    assert payload is None
    assert error == "El token ha expirado"


def test_verificar_token_rejects_signature_tampering():
    access_token, _ = run(jwt_service.generar_tokens(1, "administrador", "administrador", role_id=1))
    header, payload_part, signature = access_token.split(".")
    # Se altera un caracter del MEDIO de la firma (no el ultimo): en base64url
    # el ultimo caracter a veces solo codifica bits de relleno, por lo que
    # cambiarlo no siempre altera el valor real de la firma (test inestable).
    mid = len(signature) // 2
    replacement = "A" if signature[mid] != "A" else "B"
    flipped_signature = signature[:mid] + replacement + signature[mid + 1:]
    tampered_token = f"{header}.{payload_part}.{flipped_signature}"

    payload, error = run(jwt_service.verificar_token(tampered_token, "access"))

    assert payload is None
    assert error == "Token inválido"


def test_verificar_token_rejects_token_signed_with_foreign_key():
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    foreign_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    foreign_pem = foreign_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    now = int(time.time())
    forged_payload = {
        "sub": "1",
        "username": "administrador",
        "type": "access",
        "role": "administrador",
        "role_id": 1,
        "exp": now + 900,
        "iat": now,
    }
    forged_token = pyjwt.encode(forged_payload, foreign_pem, algorithm=jwt_service.ALGORITHM)

    payload, error = run(jwt_service.verificar_token(forged_token, "access"))

    assert payload is None
    assert error == "Token inválido"

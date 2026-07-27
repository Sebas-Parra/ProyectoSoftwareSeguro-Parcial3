import asyncio
import time

import jwt as pyjwt

from services import jwt_service


def run(coro):
    return asyncio.run(coro)


def _sign(payload, key):
    return pyjwt.encode(payload, key, algorithm="RS256")


def test_load_key_accepts_raw_pem_content_directly():
    """En Railway sale_service no comparte filesystem con auth-service, asi
    que la variable de entorno lleva el contenido PEM completo."""
    raw_pem = jwt_service.PUBLIC_KEY
    loaded = jwt_service._load_key(raw_pem)
    assert loaded == raw_pem.replace("\\n", "\n")


def test_load_key_fixes_escaped_newlines_in_raw_content():
    fake_pem_with_escaped_newlines = "-----BEGIN PUBLIC KEY-----\\nABC123\\n-----END PUBLIC KEY-----\\n"
    loaded = jwt_service._load_key(fake_pem_with_escaped_newlines)
    assert "\\n" not in loaded
    assert "\n" in loaded


def test_verificar_token_accepts_token_signed_by_master(master_private_key):
    now = int(time.time())
    payload = {
        "sub": "1",
        "username": "vendedor",
        "role": "vendedor",
        "role_id": 5,
        "type": "access",
        "exp": now + 900,
        "iat": now,
    }
    token = _sign(payload, master_private_key)

    result, error = run(jwt_service.verificar_token(token, "access"))

    assert error is None
    assert result["role_id"] == 5


def test_verificar_token_rejects_expired_token(master_private_key):
    now = int(time.time())
    payload = {
        "sub": "1", "username": "vendedor", "type": "access",
        "exp": now - 60, "iat": now - 120,
    }
    token = _sign(payload, master_private_key)

    result, error = run(jwt_service.verificar_token(token, "access"))

    assert result is None
    assert error == "El token ha expirado"


def test_verificar_token_rejects_token_not_signed_by_master():
    """Zero Trust: sale_service solo confia en tokens firmados con la llave privada del Master."""
    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization

    foreign_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    foreign_pem = foreign_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    now = int(time.time())
    payload = {
        "sub": "1", "username": "vendedor", "role_id": 5, "type": "access",
        "exp": now + 900, "iat": now,
    }
    forged_token = _sign(payload, foreign_pem)

    result, error = run(jwt_service.verificar_token(forged_token, "access"))

    assert result is None
    assert error == "Token inválido"

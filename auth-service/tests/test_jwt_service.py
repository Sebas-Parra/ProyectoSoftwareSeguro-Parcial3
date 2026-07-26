import asyncio
import time

import jwt as pyjwt

from services import jwt_service


def run(coro):
    return asyncio.run(coro)


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
    assert access_payload["role"] == "administrador"

    refresh_payload, error = run(jwt_service.verificar_token(refresh_token, "refresh"))
    assert error is None
    assert refresh_payload["jti"] == access_payload["jti"]


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
    flipped_signature = signature[:-1] + ("A" if signature[-1] != "A" else "B")
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

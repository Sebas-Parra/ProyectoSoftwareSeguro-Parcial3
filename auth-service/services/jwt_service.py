import asyncio
import token

import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
import uuid
from config.redis_cache import redis_client
from repositories import user_repository
from sqlalchemy.orm import Session
from functools import partial

load_dotenv()

ECUADOR_TZ = ZoneInfo(os.getenv("ECUADOR_TZ", "America/Guayaquil"))  # Zona horaria de Ecuador

# Cargar rutas desde el .env
PRIVATE_KEY_PATH = os.getenv("PRIVATE_KEY")

PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY")

# Leer el contenido de las llaves
with open(PRIVATE_KEY_PATH, "r") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "r") as f:
    PUBLIC_KEY = f.read()

ALGORITHM = os.getenv("ALGORITHM", "RS256")

async def generar_temptoken(usuario_id: int, username: str):
    """Genera temp (15 min) usando firma RSA."""
    now = datetime.now(ECUADOR_TZ)
    
    # Access Token
    temp_payload = {
        "sub": str(usuario_id),
        "username": username,
        "type": "access",
        "exp": now + timedelta(minutes=15),
        "iat": now
    }

    loop = asyncio.get_running_loop()
    
    temp_token = await loop.run_in_executor(None, partial(jwt.encode, temp_payload, PRIVATE_KEY, algorithm=ALGORITHM))
    
    return temp_token

async def generar_tokens(usuario_id: int, username: str, role: str, role_id: int):
    """Genera access (15 min) y refresh (7 días) usando firma RSA."""
    now = datetime.now(ECUADOR_TZ)
    jti = str(uuid.uuid4())


    redis_client.setex(f"refresh_token:{jti}", timedelta(days=7), str(usuario_id))
    
    # Access Token
    access_payload = {
        "sub": str(usuario_id),
        "username": username,
        "jti": jti,
        "role": role,
        "role_id": role_id,
        "type": "access",
        "exp": now + timedelta(minutes=15),
        "iat": now
    }
    
    # Refresh Token
    refresh_payload = {
        "sub": str(usuario_id),
        "username": username,
        "jti": jti,
        "role": role,
        "role_id": role_id,
        "type": "refresh",
        "exp": now + timedelta(days=7),
        "iat": now
    }

    loop = asyncio.get_running_loop()
    
    access_token = await loop.run_in_executor(None, partial(jwt.encode, access_payload, PRIVATE_KEY, algorithm=ALGORITHM))
    refresh_token = await loop.run_in_executor(None, partial(jwt.encode, refresh_payload, PRIVATE_KEY, algorithm=ALGORITHM))
    
    return access_token, refresh_token


async def validar_refresh_token(token_refresh):
    """Valida un refresh token y genera un nuevo par de tokens."""
    payload, error = await verificar_token(token_refresh, "refresh")
    if error: return None, error
    
    jti = payload.get("jti")
    
    exists = redis_client.exists(f"refresh_token:{jti}")
    
    if not exists:
        return None, "Token ya utilizado o revocado"
    
    redis_client.delete(f"refresh_token:{jti}")
    
    return await generar_tokens(int(payload["sub"]), payload["username"], payload["role"], payload["role_id"]), None

async def delete_tokens(jti):
    """Elimina un refresh token de Redis."""
    redis_client.delete(f"refresh_token:{jti}")

async def verificar_token(token: str, tipo_esperado: str):
    """Verifica el token usando la llave pública."""
    try:
        # Se usa PUBLIC_KEY para verificar que fue firmado por nuestra PRIVATE_KEY
        loop = asyncio.get_running_loop()
        payload = await loop.run_in_executor(None, partial(jwt.decode, token, PUBLIC_KEY, algorithms=[ALGORITHM], options={"verify_exp": True, "verify_iat": True}))

        print(f"Payload decodificado: {payload}")
        
        if payload.get("type") != tipo_esperado:
            return None, "Tipo de token incorrecto"
            
        return payload, None
    except jwt.ExpiredSignatureError as e:
        # print(e)
        return None, "El token ha expirado"
    except jwt.InvalidTokenError as e:
        # print(e)
        return None, "Token inválido"

async def verificar_token_administrador(db: Session, token: str):
    payload, error = await verificar_token(token, "access")

    if error:
        return None, error

    response = await user_repository.get_user_roles(db, int(payload["sub"]))

    if not response:
        return None, "Usuario no tiene roles asignados"

    if not any(role["id"] == 1 for role in response):
        return None, "Usuario no tiene rol de administrador"

    return payload, None
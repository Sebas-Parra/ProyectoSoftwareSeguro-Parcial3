import asyncio
import jwt
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from functools import partial

load_dotenv()

ECUADOR_TZ = ZoneInfo(os.getenv("ECUADOR_TZ", "America/Guayaquil"))  # Zona horaria de Ecuador


PUBLIC_KEY_PATH = os.getenv("PUBLIC_KEY")


with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()

ALGORITHM = os.getenv("ALGORITHM", "RS256")

async def verificar_token(token: str, tipo_esperado: str):
    """Verifica el token usando la llave pública."""
    try:
        # Se usa PUBLIC_KEY para verificar que fue firmado por nuestra PRIVATE_KEY
        loop = asyncio.get_running_loop()
        payload = await loop.run_in_executor(None, partial(jwt.decode, token, PUBLIC_KEY, algorithms=[ALGORITHM], options={"verify_exp": True, "verify_iat": True}))
        
        if payload.get("type") != tipo_esperado:
            return None, "Tipo de token incorrecto"
            
        return payload, None
    except jwt.ExpiredSignatureError as e:
        # print(e)
        return None, "El token ha expirado"
    except jwt.InvalidTokenError as e:
        print(e)
        return None, "Token inválido"

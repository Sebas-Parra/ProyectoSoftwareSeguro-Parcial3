import asyncio
import jwt
import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo
from functools import partial

load_dotenv()

ECUADOR_TZ = ZoneInfo(os.getenv("ECUADOR_TZ", "America/Guayaquil"))  # Zona horaria de Ecuador


def _load_key(env_value: str) -> str:
    """Acepta el contenido PEM directo (ej. en Railway se pega la llave
    completa como valor de la variable, ya que los servicios no comparten
    filesystem) o una ruta a un archivo .pem (desarrollo local, apuntando
    a shared-keys/)."""
    if env_value and env_value.strip().startswith("-----BEGIN"):
        return env_value.replace("\\n", "\n")
    with open(env_value, "r") as f:
        return f.read()


PUBLIC_KEY = _load_key(os.getenv("PUBLIC_KEY"))

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

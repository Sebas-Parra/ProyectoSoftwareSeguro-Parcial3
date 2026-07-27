import redis
import os
from dotenv import load_dotenv

load_dotenv()

# Si REDIS_URL esta definida (ej. "rediss://default:<password>@<host>:<port>",
# como la da Upstash/Redis Cloud) se usa directo: soporta password y TLS,
# necesarios para Redis administrado en la nube. En local (docker-compose,
# sin password ni TLS) se sigue usando REDIS_HOST/PORT/DB.
def _build_redis_client(redis_url: str, host: str, port: int, db: int):
    if redis_url:
        return redis.from_url(redis_url, decode_responses=True)
    return redis.StrictRedis(host=host, port=port, db=db, decode_responses=True)


REDIS_URL = os.getenv("REDIS_URL")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

redis_client = _build_redis_client(REDIS_URL, REDIS_HOST, REDIS_PORT, REDIS_DB)

def test_connection():
    try:
        return redis_client.ping()
    except redis.ConnectionError:
        return False

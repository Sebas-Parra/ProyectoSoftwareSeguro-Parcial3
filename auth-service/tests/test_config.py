from tests.db_helpers import run
from config.database import get_db
from config.redis_cache import test_connection as check_redis_connection, _build_redis_client


def test_get_db_yields_a_session_and_closes_cleanly():
    async def scenario():
        gen = get_db()
        session = await gen.__anext__()
        assert session is not None
        await gen.aclose()

    run(scenario())


def test_redis_test_connection_returns_bool():
    result = check_redis_connection()
    assert isinstance(result, bool)


def test_build_redis_client_uses_url_when_present():
    """Upstash/Redis Cloud (produccion) dan una unica URL con password y
    TLS (rediss://...); debe tener prioridad sobre host/port/db sueltos."""
    client = _build_redis_client("redis://localhost:6379/0", "otro-host", 1111, 5)
    assert client.connection_pool.connection_kwargs.get("host") == "localhost"


def test_build_redis_client_falls_back_to_host_port_db():
    client = _build_redis_client(None, "localhost", 6379, 0)
    assert client.connection_pool.connection_kwargs.get("host") == "localhost"
    assert client.connection_pool.connection_kwargs.get("port") == 6379

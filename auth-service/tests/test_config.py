from tests.db_helpers import run
from config.database import get_db
from config.redis_cache import test_connection as check_redis_connection


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

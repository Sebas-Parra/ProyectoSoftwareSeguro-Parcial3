import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.database import Base
import models  # noqa: F401


def run(coro):
    return asyncio.run(coro)


async def make_sqlite_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    return engine, session_factory()


class DbCase:
    async def __aenter__(self):
        self.engine, self.db = await make_sqlite_session()
        return self.db

    async def __aexit__(self, exc_type, exc, tb):
        await self.db.close()
        await self.engine.dispose()

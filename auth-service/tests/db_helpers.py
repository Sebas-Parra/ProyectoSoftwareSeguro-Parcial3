import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.database import Base
# Aseguramos que TODOS los modelos (incluido RoleMenu, que ningun modulo
# de la app importa explicitamente) esten registrados en Base.metadata
# antes de crear las tablas.
import models  # noqa: F401
from models.role_menu_model import RoleMenu  # noqa: F401


def run(coro):
    return asyncio.run(coro)


async def make_sqlite_session():
    """Crea un engine + sesion SQLite en memoria con todas las tablas creadas.

    Se usa para probar los repositorios (consultas SQL reales, incluida la
    CTE recursiva de menus) sin depender de un Postgres real en CI.
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
    return engine, session_factory()


class DbCase:
    """Context manager que crea una sesion SQLite fresca y la cierra al salir."""

    async def __aenter__(self):
        self.engine, self.db = await make_sqlite_session()
        return self.db

    async def __aexit__(self, exc_type, exc, tb):
        await self.db.close()
        await self.engine.dispose()

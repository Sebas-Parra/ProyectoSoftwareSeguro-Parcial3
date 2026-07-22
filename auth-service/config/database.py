import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

load_dotenv()

# Asegúrate de que tu variable de entorno en .env use un driver async 
# Ej: postgresql+asyncpg://user:pass@localhost/db
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 1. Crear el motor asíncrono
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 2. Crear la fábrica de sesiones asíncronas
AsyncSessionLocal = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

Base = declarative_base()

# 3. Dependencia de base de datos correcta
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
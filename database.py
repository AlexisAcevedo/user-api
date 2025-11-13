# database.py
"""
Configuración de la base de datos con SQLAlchemy.
Maneja la conexión async a PostgreSQL.
"""
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Usa variables de entorno para la configuración de la base de datos.
# Formato: "postgresql+asyncpg://USUARIO:CONTRASEÑA@HOST:PUERTO/NOMBRE_DB"
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("La variable de entorno DATABASE_URL no está configurada. Asegúrate de que el archivo .env exista y se cargue correctamente.")

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    """Dependencia para obtener la sesión de la base de datos."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
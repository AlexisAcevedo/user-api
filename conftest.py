"""
Configuración de pytest para la suite de tests.
"""
import pytest
import pytest_asyncio
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from main import app, get_db
from database import Base

# Configuración de base de datos de prueba
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Crea el engine de base de datos para pruebas."""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine):
    """Proporciona una sesión de base de datos para cada test."""
    TestingSessionLocal = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with TestingSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest.fixture(autouse=True)
def override_get_db_fixture(db_session):
    """Overrides la dependencia get_db con la sesión de prueba."""
    async def get_db_override():
        yield db_session
    
    app.dependency_overrides[get_db] = get_db_override
    yield
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def disable_rate_limiting():
    """Desactiva el rate limiting durante los tests."""
    from main import limiter
    
    # Guardamos el estado original
    original_enabled = limiter.enabled
    
    # Desactivamos el rate limiting
    limiter.enabled = False
    
    yield
    
    # Restauramos el estado original
    limiter.enabled = original_enabled

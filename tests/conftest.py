from pathlib import Path

from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from charity_project_app.core import db_manager
from charity_project_app.core.base import Base
from charity_project_app.main import main_app

pytest_plugins = ["fixtures.data"]

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
TEST_DB = BASE_DIR / "test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{str(TEST_DB)}"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = async_sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    bind=engine,
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def test_client():
    main_app.dependency_overrides[db_manager.get_session] = override_db
    with TestClient(main_app) as client:
        yield client


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=main_app, base_url="http://test") as ac:
        yield ac

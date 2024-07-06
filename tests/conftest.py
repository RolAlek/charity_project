from pathlib import Path

from fastapi.testclient import TestClient
import pytest_asyncio
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from charity_project_app.main import main_app
from charity_project_app.core.base import Base
from charity_project_app.core import db_manager


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
TEST_DB = BASE_DIR / 'test.db'
SQLALCHEMY_DATABASE_URL = f'sqlite+aiosqlite:///{str(TEST_DB)}'
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
)
TestingSessionLocal = async_sessionmaker(
    class_=AsyncSession, autocommit=False, autoflush=False, bind=engine,
)


async def override_db():
    async with TestingSessionLocal() as session:
        yield session

main_app.dependency_overrides[db_manager.get_session] = override_db


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

client = TestClient(main_app)


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=main_app, base_url="http://test") as ac:
        yield ac

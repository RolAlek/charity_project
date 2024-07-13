from pathlib import Path

import pytest
import pytest_asyncio
from app.core.base import Base
from app.main import main_app
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

pytest_plugins = ["fixtures.data", "fixtures.user"]

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


@pytest.fixture()
async def async_client():
    async with AsyncClient(app=main_app, base_url="http://test") as ac:
        yield ac

from datetime import datetime
from typing import AsyncGenerator

from core.config import settings
from sqlalchemy import CheckConstraint
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
)


class Base(DeclarativeBase):
    __abstract__ = True

    @classmethod
    @declared_attr
    def __tablename__(cls):
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(primary_key=True)


class CommonFields:
    full_amount: Mapped[int] = mapped_column(
        CheckConstraint("full_amount > 0")
    )
    created_date: Mapped[datetime] = mapped_column(default=datetime.now)
    invested_amount: Mapped[int] = mapped_column(default=0)
    fully_invested: Mapped[bool] = mapped_column(default=False)
    close_date: Mapped[datetime] = mapped_column(nullable=True)


class DBManager:

    def __init__(self, url):
        self.engine = create_async_engine(url)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_factory() as session:
            yield session

    async def dispose(self) -> None:
        await self.engine.dispose()


db_manager = DBManager(str(settings.db.url))

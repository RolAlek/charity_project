import contextlib
from datetime import datetime

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core import db_manager
from app.core.config import settings
from app.core.users import get_user_db, get_user_manager
from app.schemas import UserCreate

get_async_session_context = contextlib.asynccontextmanager(
    db_manager.get_session
)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def crate_user(
    email: EmailStr,
    first_name: str,
    last_name: str,
    birthday: datetime.date,
    password: str,
    is_superuser: bool = False,
) -> None:
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    await user_manager.create(
                        UserCreate(
                            email=email,
                            password=password,
                            is_superuser=is_superuser,
                            first_name=first_name,
                            last_name=last_name,
                            birthday=birthday,
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser() -> None:
    if settings.user.init_root:
        await crate_user(
            email=settings.user.root.login,
            password=settings.user.root.password,
            is_superuser=True,
            first_name=settings.user.root.first_name,
            last_name=settings.user.root.last_name,
            birthday=settings.user.root.birthday,
        )

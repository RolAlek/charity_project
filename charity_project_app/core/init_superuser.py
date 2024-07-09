import contextlib

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from charity_project_app.core import db_manager
from charity_project_app.core.config import settings
from charity_project_app.core.users import get_user_db, get_user_manager
from charity_project_app.schemas import UserCreate

get_async_session_context = contextlib.asynccontextmanager(
    db_manager.get_session
)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def crate_user(
    email: EmailStr,
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
                        )
                    )
    except UserAlreadyExists:
        pass


async def create_first_superuser() -> None:
    if (
        settings.user.superuser_login is not None
        and settings.user.superuser_password is not None
    ):
        await crate_user(
            email=settings.user.superuser_login,
            password=settings.user.superuser_password,
            is_superuser=True,
        )

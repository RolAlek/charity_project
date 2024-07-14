from typing import Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_manager
from core.config import settings
from models import User
from schemas import UserCreate


async def get_user_db(
    session: AsyncSession = Depends(db_manager.get_session),
):
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="/api/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.user.secret,
        lifetime_seconds=settings.user.lifetime,
    )


authentication_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ):
        if len(password) < 12:
            raise InvalidPasswordException(
                reason="Password must be at least 12 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Password cannot be the same as email"
            )

    async def after_register(
        self,
        user: User,
        request: Request | None = None,
    ):
        print(f"Пользователь {user.email} зарегистрирован.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [authentication_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

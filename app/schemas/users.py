from datetime import datetime

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    birthday: datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str
    birthday: datetime


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str | None = None
    last_name: str | None = None
    birthday: datetime | None = None

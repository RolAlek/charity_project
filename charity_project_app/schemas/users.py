from datetime import datetime

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str
    birthdate: datetime


class UserCreate(schemas.BaseUserCreate):
    first_name: str | None = None
    last_name: str | None = None
    birthdate: datetime | None = None


class UserUpdate(schemas.BaseUserUpdate):
    first_name: str
    last_name: str
    birthdate: datetime

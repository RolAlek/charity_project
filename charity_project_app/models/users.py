from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from charity_project_app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    birthday: Mapped[datetime] = mapped_column(Date)

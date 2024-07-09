from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column

from charity_project_app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    birthday: Mapped[datetime] = mapped_column(nullable=True)

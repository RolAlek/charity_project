from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base, CommonFields


class Project(Base, CommonFields):

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]

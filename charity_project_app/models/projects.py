from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from charity_project_app.core.db import Base


class Project(Base):

    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str]
    full_amount: Mapped[int]
    invested_amount: Mapped[int] = mapped_column(default=0)
    fully_invested: Mapped[bool] = mapped_column(default=False)
    created_date: Mapped[datetime] = mapped_column(default=datetime.now)
    close_date: Mapped[datetime] = mapped_column(nullable=True)

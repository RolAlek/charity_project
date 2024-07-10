from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from charity_project_app.core.db import Base, CommonFields


class Donation(Base, CommonFields):
    comment: Mapped[str] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

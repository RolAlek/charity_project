from datetime import datetime

from pydantic import BaseModel, Field, PositiveInt


class CreateDonation(BaseModel):
    full_amount: PositiveInt
    comment: str | None = Field(None, min_length=1)


class ReadUserDonation(CreateDonation):
    id: int
    created_date: datetime


class ReadSuperUserDonation(ReadUserDonation):
    user_id: int
    invested_amount: int
    fully_invested: bool
    closed_date: datetime | None = None

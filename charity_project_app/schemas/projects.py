from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreateProject(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class ReadProject(CreateProject):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invested_amount: int
    fully_invested: bool
    created_date: datetime
    close_data: datetime | None = None

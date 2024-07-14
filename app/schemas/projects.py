from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    Extra,
    Field,
    PositiveInt,
    field_validator,
)


class CreateProject(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class ReadProject(CreateProject):
    model_config = ConfigDict(from_attributes=True)

    id: int
    invested_amount: int
    fully_invested: bool
    created_date: datetime
    close_date: datetime


class UpdateProject(CreateProject):
    model_config = ConfigDict(extra=Extra.forbid)
    name: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, min_length=1)
    full_amount: PositiveInt | None = None

    @classmethod
    @field_validator("name", "description", "full_amount")
    def columns_cant_be_null(cls, value):
        if value is None:
            raise ValueError("Column can not be null")
        return value

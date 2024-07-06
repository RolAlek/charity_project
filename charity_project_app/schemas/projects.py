from pydantic import BaseModel, Field


class CreateProject(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

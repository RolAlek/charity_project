from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.models import Project


async def validate_unique_project_name(name: str, session: AsyncSession):
    if await session.scalar(select(Project).where(Project.name == name)):
        raise HTTPException(
            status_code=400,
            detail="Project with this name already exists",
        )

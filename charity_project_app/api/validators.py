from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.crud import project_crud
from charity_project_app.models import Project


async def validate_unique_project_name(name: str, session: AsyncSession):
    if await session.scalar(select(Project).where(Project.name == name)):
        raise HTTPException(
            status_code=400,
            detail="Project with this name already exists",
        )


async def check_project_exists(project_id: int, session: AsyncSession):
    project = await project_crud.get_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )
    return project

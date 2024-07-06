from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.api.validators import validate_unique_project_name
from charity_project_app.core import db_manager
from charity_project_app.crud import project_crud
from charity_project_app.schemas import CreateProject

router = APIRouter()


@router.post("/", status_code=201)
async def create_project(
    new_project: CreateProject,
    session: AsyncSession = Depends(db_manager.get_session),
):
    await validate_unique_project_name(new_project.name, session)
    return await project_crud.create(new_project, session)

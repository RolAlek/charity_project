from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.api.validators import validate_unique_project_name
from charity_project_app.core import db_manager
from charity_project_app.crud import project_crud
from charity_project_app.schemas import CreateProject, ReadProject

router = APIRouter()


@router.post(
    "/",
    status_code=201,
    response_model=ReadProject,
    response_model_exclude_none=True,
)
async def create_project(
    new_project: CreateProject,
    session: AsyncSession = Depends(db_manager.get_session),
):
    await validate_unique_project_name(new_project.name, session)
    return await project_crud.create(new_project, session)


@router.get(
    "/",
    response_model=list[ReadProject],
    response_model_exclude_none=True,
)
async def get_projects(
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await project_crud.read_all(session)


@router.get(
    "/{project_id}",
    response_model=ReadProject,
    response_model_exclude_none=True,
)
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await project_crud.read(project_id, session)

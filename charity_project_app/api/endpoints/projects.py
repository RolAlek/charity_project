from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.api.validators import (
    check_project_exists,
    validate_unique_project_name,
)
from charity_project_app.core import db_manager
from charity_project_app.crud import project_crud
from charity_project_app.schemas import (
    CreateProject,
    ReadProject,
    UpdateProject,
)

router = APIRouter()


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
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
    return await project_crud.get_all(session)


@router.get(
    "/{project_id}",
    response_model=ReadProject,
    response_model_exclude_none=True,
)
async def get_project(
    project_id: int,
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await project_crud.get_by_id(project_id, session)


@router.patch(
    "/{project_id}",
    response_model=ReadProject,
    response_model_exclude_none=True,
)
async def update_project(
    project_id: int,
    project_in: UpdateProject,
    session: AsyncSession = Depends(db_manager.get_session),
):
    if project_in.name is not None:
        await validate_unique_project_name(project_in.name, session)

    return await project_crud.update_project(
        await check_project_exists(project_id, session),
        project_in,
        session,
    )


@router.delete("/{project_id}", status_code=HTTPStatus.NO_CONTENT)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(db_manager.get_session),
):
    await project_crud.delete_project(
        await check_project_exists(project_id, session),
        session,
    )

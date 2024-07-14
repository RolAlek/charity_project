from http import HTTPStatus

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.invest_logic import make_distribution
from api.validators import (
    check_project_before_delete,
    check_project_before_update,
    validate_unique_project_name,
)
from core import db_manager
from core.users import current_superuser
from crud import project_crud
from schemas import CreateProject, ReadProject, UpdateProject

router = APIRouter()


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    response_model=ReadProject,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_project(
    new_project: CreateProject,
    session: AsyncSession = Depends(db_manager.get_session),
):
    await validate_unique_project_name(new_project.name, session)
    project = await project_crud.create(new_project, session)
    return await make_distribution(project, session)


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
    dependencies=[Depends(current_superuser)],
)
async def update_project(
    project_id: int,
    project_in: UpdateProject,
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await project_crud.update_project(
        await check_project_before_update(
            project_id,
            session,
            **project_in.model_dump(exclude_unset=True),
        ),
        project_in,
        session,
    )


@router.delete(
    "/{project_id}",
    status_code=HTTPStatus.NO_CONTENT,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(db_manager.get_session),
):
    await project_crud.delete_project(
        await check_project_before_delete(project_id, session),
        session,
    )

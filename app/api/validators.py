from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud import project_crud
from models import Project


async def validate_unique_project_name(
    name: str, session: AsyncSession
) -> None:
    if await session.scalar(select(Project).where(Project.name == name)):
        raise HTTPException(
            status_code=400,
            detail="Project with this name already exists.",
        )


async def check_project_exists(
    project_id: int, session: AsyncSession
) -> Project:
    project = await project_crud.get_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Project not found",
        )
    return project


async def check_project_before_delete(
    project_id: int,
    session: AsyncSession,
) -> Project:
    project = await check_project_exists(project_id, session)
    if project.invested_amount > 0 or project.close_date:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "You can't delete a closed project or a project in which"
                "funds have been invested."
            ),
        )
    return project


async def check_project_before_update(
    project_id: int,
    session: AsyncSession,
    **kwargs,
):
    project = await check_project_exists(project_id, session)

    if project.close_date is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="You can't update a closed project.",
        )

    if kwargs.get("name") is not None:
        await validate_unique_project_name(kwargs["name"], session)

    if kwargs.get("full_amount") is not None:
        if kwargs["full_amount"] < project.invested_amount:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail=(
                    "You can't update a `full_amount` field to less then the"
                    "`invested_amount` in this project."
                ),
            )
    return project

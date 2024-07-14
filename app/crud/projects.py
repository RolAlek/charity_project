from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Project
from app.schemas import UpdateProject

from .base import CRUDManager


class ProjectCRUD(CRUDManager):
    @staticmethod
    async def update_project(
        project: Project,
        project_in: UpdateProject,
        session: AsyncSession,
    ):
        obj_data = jsonable_encoder(project)
        update_data = project_in.model_dump(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(project, field, update_data[field])

        session.add(project)
        await session.commit()
        await session.refresh(project)

        return project

    @staticmethod
    async def delete_project(project: Project, session: AsyncSession):
        await session.delete(project)
        await session.commit()

    @staticmethod
    async def get_completed_project_by_rate(session: AsyncSession):
        projects = await session.execute(
            select(
                Project.name,
                (Project.close_date - Project.created_date).label("rate"),
                Project.description,
            )
            .where(Project.fully_invested.is_(True))
            .order_by("rate")
        )
        return [
            {
                "name": project[0],
                "rate": str(project[1]),
                "description": project[2],
            }
            for project in projects.fetchall()
        ]


crud_manager = ProjectCRUD(Project)

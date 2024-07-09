from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.models import Project
from charity_project_app.schemas import UpdateProject

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


crud_manager = ProjectCRUD(Project)

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.models import User


class CRUDManager:

    def __init__(self, model):
        self.model = model

    async def create(self, data, session: AsyncSession):
        new_data = data.model_dump()
        db_obj = self.model(**new_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_all(self, session: AsyncSession, user: User | None = None):
        stmt = select(self.model)
        if user is not None:
            stmt = stmt.where(self.model.user_id == user.id)
        objects = await session.scalars(stmt)
        return objects.all()

    async def get_by_id(self, obj_id: int, session: AsyncSession):
        return await session.get(self.model, obj_id)

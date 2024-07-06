from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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

    async def read_all(self, session: AsyncSession):
        objects = await session.scalars(select(self.model))
        return objects.all()

    async def read(self, obj_id: int, session: AsyncSession):
        return await session.get(self.model, obj_id)

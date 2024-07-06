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

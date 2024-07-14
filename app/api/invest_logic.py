from datetime import datetime

from sqlalchemy import ScalarResult, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Donation, Project


async def get_distributions_objects(
    model: Donation | Project,
    session: AsyncSession,
) -> ScalarResult[Donation | Project]:
    model_class = Donation if isinstance(model, Project) else Project
    distributions = await session.scalars(
        select(model_class)
        .where(model_class.close_date.is_(None))
        .order_by(model_class.created_date)
    )
    return distributions


async def make_distribution(obj: Donation | Project, session: AsyncSession):
    for_distribution = await get_distributions_objects(obj, session)

    if for_distribution is None:
        return obj

    for distribution in for_distribution:
        available = obj.full_amount - obj.invested_amount
        necessary_funds = (
            distribution.full_amount - distribution.invested_amount
        )

        if available > necessary_funds:
            distribution.invested_amount += necessary_funds
            obj.invested_amount += necessary_funds
        else:
            distribution.invested_amount += available
            obj.invested_amount += available

        distribution.fully_invested = (
            distribution.invested_amount == distribution.full_amount
        )
        distribution.close_date = (
            datetime.now() if distribution.fully_invested else None
        )

        obj.fully_invested = obj.full_amount == obj.invested_amount
        obj.close_date = datetime.now() if obj.fully_invested else None

        session.add(distribution)

    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.invest_logic import make_distribution
from app.core import db_manager
from app.core.users import current_superuser, current_user
from app.crud import donate_crud
from app.models import User
from app.schemas import (
    CreateDonation,
    ReadSuperUserDonation,
    ReadUserDonation,
)

router = APIRouter()


@router.post(
    "/",
    response_model=ReadUserDonation,
    status_code=201,
    response_model_exclude_none=True,
)
async def make_a_donation(
    donation: CreateDonation,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_manager.get_session),
):
    donation = await donate_crud.create(donation, session, user=user)
    return await make_distribution(donation, session)


@router.get(
    "/",
    response_model=list[ReadSuperUserDonation],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await donate_crud.get_all(session)


@router.get(
    "/my",
    response_model=list[ReadUserDonation],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await donate_crud.get_all(user, session)

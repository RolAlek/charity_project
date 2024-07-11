from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from charity_project_app.core import db_manager
from charity_project_app.core.users import current_superuser, current_user
from charity_project_app.crud import donate_crud
from charity_project_app.models import User
from charity_project_app.schemas import (
    CreateDonation,
    ReadSuperUserDonation,
    ReadUserDonation,
)

router = APIRouter()


@router.post("/", response_model=ReadUserDonation)
async def make_a_donation(
    donation: CreateDonation,
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await donate_crud.create(donation, session)


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
    response_model=[ReadUserDonation],
    dependencies=[Depends(current_user)],
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(db_manager.get_session),
):
    return await donate_crud.get_all(user, session)

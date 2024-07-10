from fastapi import APIRouter, Depends

from charity_project_app.core import db_manager
from charity_project_app.crud import donate_crud
from charity_project_app.schemas import CreateDonation, ReadUserDonation

router = APIRouter()


@router.post("/", response_model=ReadUserDonation)
async def make_a_donation(
    donation: CreateDonation,
    session=Depends(db_manager.get_session),
):
    return await donate_crud.create(donation, session)

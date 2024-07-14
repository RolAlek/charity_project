from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_manager
from core.google_client import get_google_client
from core.users import current_superuser
from crud import project_crud
from services.google_api import (
    create_spreadsheet,
    set_user_permissions,
    spreadsheet_update_values,
)

router = APIRouter()


@router.post(
    "/",
    response_model=list[dict[str, str]],
    dependencies=[Depends(current_superuser)],
)
async def get_report(
    session: AsyncSession = Depends(db_manager.get_session),
    wrapp_services: Aiogoogle = Depends(get_google_client),
):
    projects = await project_crud.get_completed_project_by_rate(session)
    spreadsheet_id = await create_spreadsheet(wrapp_services)
    await set_user_permissions(wrapp_services, spreadsheet_id)
    await spreadsheet_update_values(spreadsheet_id, projects, wrapp_services)
    return projects

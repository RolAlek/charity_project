from fastapi import FastAPI

from api import main_router
from core import db_manager
from core.config import settings
from core.init_superuser import create_first_superuser

main_app = FastAPI(
    title=settings.app_title,
)

main_app.include_router(main_router, prefix="/api")


@main_app.on_event("startup")
async def startup_event():
    await create_first_superuser()


@main_app.on_event("shutdown")
async def shutdown_event():
    await db_manager.dispose()

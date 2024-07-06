from contextlib import asynccontextmanager

from fastapi import FastAPI

from charity_project_app.api import main_router
from charity_project_app.core import db_manager
from charity_project_app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start the app
    yield
    # stop the app
    await db_manager.dispose()


main_app = FastAPI(
    title=settings.app_title,
    lifespan=lifespan,
)
main_app.include_router(main_router, prefix="/api")

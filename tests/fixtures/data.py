from datetime import datetime

import pytest
from sqlalchemy import insert
from tests.conftest import TestingSessionLocal

from charity_project_app.models import Project


@pytest.fixture
async def charity_project_first(freezer):
    freezer.move_to("2023-01-01")
    async with TestingSessionLocal() as session:
        await session.execute(
            insert(Project).values(
                id=1,
                name="Test Charity Project number 1",
                description="This is a test charity project number 1",
                full_amount=1000,
                created_date=datetime.now(),
            )
        )
        await session.commit()


@pytest.fixture
async def charity_project_second(freezer):
    freezer.move_to("2023-01-01")
    async with TestingSessionLocal() as session:
        await session.execute(
            insert(Project).values(
                id=2,
                name="Test Charity Project number 2",
                description="This is a test charity project number 2",
                full_amount=2000,
                created_date=datetime.now(),
            )
        )
        await session.commit()

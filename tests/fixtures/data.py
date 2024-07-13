from datetime import datetime

import pytest
from app.models import Donation, Project
from sqlalchemy import insert
from tests.conftest import TestingSessionLocal


@pytest.fixture
async def charity_project_first(freezer):
    freezer.move_to("2023-01-01")
    async with TestingSessionLocal() as session:
        project = Project(
            id=1,
            name="Test Charity Project number 1",
            description="This is a test charity project number 1",
            full_amount=1000,
            created_date=datetime.now(),
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project


@pytest.fixture
async def charity_project_second(freezer):
    freezer.move_to("2023-02-01")
    async with TestingSessionLocal() as session:
        project = Project(
            id=2,
            name="Test Charity Project number 2",
            description="This is a test charity project number 2",
            full_amount=2000,
            created_date=datetime.now(),
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project


@pytest.fixture
async def charity_project_with_invested_amount(freezer):
    freezer.move_to("2023-01-01")
    async with TestingSessionLocal() as session:
        await session.execute(
            insert(Project).values(
                id=3,
                name="Test Charity Project number 3",
                description=(
                    "This is a test charity project number 3 to testing"
                    " full_amount with invested_amount"
                ),
                full_amount=1000,
                invested_amount=600,
                created_date=datetime.now(),
            ),
        )
        await session.commit()


@pytest.fixture
async def closed_charity_project(freezer):
    freezer.move_to("2023-01-01")
    async with TestingSessionLocal() as session:
        await session.execute(
            insert(Project).values(
                id=4,
                name="Test Charity Project number 4",
                description="This is a closed test charity project.",
                full_amount=1000,
                invested_amount=1000,
                fully_invested=True,
                close_date=datetime.now(),
                created_date=datetime.now(),
            )
        )
        await session.commit()


@pytest.fixture
async def charity_project_little_invested(freezer):
    freezer.move_to("2023-01-01")
    async with TestingSessionLocal() as session:
        project = Project(
            id=1,
            name="Test Charity Project with little invested",
            description="This is a Test Charity Project with little invested.",
            full_amount=3000,
            invested_amount=1000,
            fully_invested=True,
            created_date=datetime.now(),
        )
        session.add(project)
        await session.commit()
        await session.refresh(project)
        return project


@pytest.fixture
def correct_create_testing_data():
    return {
        "name": "Test name",
        "description": "Test description",
        "full_amount": 1000,
    }


@pytest.fixture
def update_testing_data():
    return {"description": "Test update description"}


@pytest.fixture
async def donation(freezer):
    freezer.move_to("2023-01-01")
    async with TestingSessionLocal() as session:
        await session.execute(
            insert(Donation).values(
                id=1,
                user_id=1,
                full_amount=1000,
                created_date=datetime.now(),
            )
        )
        await session.commit()

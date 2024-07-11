from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest

from tests.conftest import override_db
from charity_project_app.core import db_manager
from charity_project_app.core.users import current_superuser, current_user
from charity_project_app.models import User
from charity_project_app.main import main_app

superuser = User(
    id=1,
    is_superuser=True,
    is_verified=True,
    is_active=True,
)
not_auth_user = User(
    id=2,
    is_superuser=False,
    is_verified=False,
    is_active=False,
)
regular_user = User(
    id=3,
    is_superuser=False,
    is_verified=True,
    is_active=True,
)


@pytest.fixture
def superuser_client():
    main_app.dependency_overrides[db_manager.get_session] = override_db
    main_app.dependency_overrides[current_superuser] = lambda: superuser
    with TestClient(main_app) as client:
        yield client


@pytest.fixture
def test_client():
    main_app.dependency_overrides[db_manager.get_session] = override_db
    main_app.dependency_overrides[current_user] = lambda: not_auth_user
    with TestClient(main_app) as client:
        yield client


@pytest.fixture
def user_client():
    def raise_forbidden():
        raise HTTPException(status_code=403, detail="Forbidden")

    main_app.dependency_overrides[db_manager.get_session] = override_db
    main_app.dependency_overrides[current_user] = lambda: regular_user
    main_app.dependency_overrides[current_superuser] = (
        lambda: raise_forbidden()
    )
    with TestClient(main_app) as client:
        yield client

from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest

from app.core import db_manager
from app.core.users import current_superuser, current_user
from app.main import main_app
from app.models import User
from tests.conftest import override_db

superuser = User(
    id=1,
    is_superuser=True,
    is_verified=True,
    is_active=True,
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
    return TestClient(main_app)


@pytest.fixture
def test_client():
    main_app.dependency_overrides[db_manager.get_session] = override_db
    return TestClient(main_app)


@pytest.fixture
def user_client():
    def raise_forbidden():
        raise HTTPException(status_code=403, detail="Forbidden")

    main_app.dependency_overrides[db_manager.get_session] = override_db
    main_app.dependency_overrides[current_user] = lambda: regular_user
    main_app.dependency_overrides[current_superuser] = (
        lambda: raise_forbidden()
    )
    return TestClient(main_app)

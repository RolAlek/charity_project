import pytest

URL = "api/projects/"


@pytest.mark.parametrize(
    "invalid_name",
    [None, "", "a" * 101],
    ids=["null", "empty", "too long"],
)
def test_create_project_with_invalid_name(invalid_name, test_client):
    response = test_client.post(
        URL,
        json={
            "name": invalid_name,
            "description": "Project test description",
            "full_amount": 1000,
        },
    )
    assert (
        response.status_code == 422
    ), "Создание проекта с пустым именем или больше 100 символов не допустимо."


@pytest.mark.parametrize(
    "non_desc",
    [None, ""],
    ids=["null", "empty"],
)
def test_create_project_with_non_description(non_desc, test_client):
    response = test_client.post(
        URL,
        json={
            "name": "Project test name",
            "description": non_desc,
            "full_amount": 1000,
        },
    )
    assert (
        response.status_code == 422
    ), "Создание проекта с пустым описанием не допустимо."


@pytest.mark.parametrize(
    "json_data",
    [
        {"invested_amount": 1000},
        {"fully_invested": True},
        {"id": 100},
    ],
)
def test_create_project_with_default_filling_fields(json_data, test_client):
    response = test_client.post(
        URL,
        json=json_data,
    )
    assert response.status_code == 422, (
        "При попытке передавать автозаполняемые поля при создании проекта"
        " должна возращать ошибка 422."
    )


@pytest.mark.parametrize(
    "invalid_amount",
    [None, "", 0, -1, "string"],
    ids=["None", "empty_string", "null", "negative", "string"],
)
def test_create_project_with_invalid_amount(invalid_amount, test_client):
    response = test_client.post(
        URL,
        json={
            "name": "Project test name",
            "description": "Project test description",
            "full_amount": invalid_amount,
        },
    )
    assert response.status_code == 422, (
        "Создание проекта с пустым, меньше 1 или строковым значением суммы не"
        " допустимо."
    )


async def test_create_project(async_client):
    response = await async_client.post(
        URL,
        json={
            "name": "Test name",
            "description": "Test description",
            "full_amount": 1000,
        },
    )
    assert (
        response.status_code == 201
    ), "Создание проекта с корректными данными не должно вызывать ошибок."
    data = response.json()
    expected_keys = {
        "name",
        "description",
        "full_amount",
        "id",
        "invested_amount",
        "fully_invested",
        "created_date",
    }
    missing_keys = expected_keys - data.keys()
    assert not missing_keys, (
        f"При коректном запросе на создание проекта к {URL} в ответе не"
        f"хватает следующих ключей: `{"`, `".join(missing_keys)}`"
    )
    data.pop("created_date")
    data.pop("close_date", None)
    assert data == {
        "id": 1,
        "name": "Test name",
        "description": "Test description",
        "full_amount": 1000,
        "fully_invested": False,
        "invested_amount": 0,
    }, (
        f"При POST-запросе к {URL} ответ отличается от ожидаемого. Убедитесь,"
        "что пустые поля не показывются в ответе"
    )


@pytest.mark.usefixtures("charity_project_first", "charity_project_second")
async def test_get_all_projects(async_client):
    response = await async_client.get(URL)
    assert (
        response.status_code == 200
    ), f"GET-запрос к {URL} должен вернуть код 200."
    data = response.json()
    [project.pop("close_date", None) for project in data]
    assert data == [
        {
            "id": 1,
            "name": "Test Charity Project number 1",
            "description": "This is a test charity project number 1",
            "full_amount": 1000,
            "created_date": "2023-01-01T00:00:00",
            "fully_invested": False,
            "invested_amount": 0,
        },
        {
            "id": 2,
            "name": "Test Charity Project number 2",
            "description": "This is a test charity project number 2",
            "full_amount": 2000,
            "created_date": "2023-01-01T00:00:00",
            "fully_invested": False,
            "invested_amount": 0,
        },
    ], f"GET-запрос к {URL} должен вернуть список существующих проектов."

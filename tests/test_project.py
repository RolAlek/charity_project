import os
import pytest

URL = "api/projects/"
EXPECTED_KEYS = {
    "name",
    "description",
    "full_amount",
    "id",
    "invested_amount",
    "fully_invested",
    "created_date",
}


@pytest.mark.parametrize(
    "invalid_name",
    [None, "", "a" * 101],
    ids=["null", "empty", "too long"],
)
def test_create_project_with_invalid_name(superuser_client, invalid_name):
    response = superuser_client.post(
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
def test_create_project_with_non_description(non_desc, superuser_client):
    response = superuser_client.post(
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
def test_create_project_with_default_filling_fields(
    json_data, superuser_client
):
    response = superuser_client.post(
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
def test_create_project_with_invalid_amount(invalid_amount, superuser_client):
    response = superuser_client.post(
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


async def test_create_project(async_client, correct_create_testing_data):
    response = await async_client.post(
        URL,
        json=correct_create_testing_data,
    )
    assert (
        response.status_code == 201
    ), "Создание проекта с корректными данными не должно вызывать ошибок."
    data = response.json()
    missing_keys = EXPECTED_KEYS - data.keys()
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


@pytest.mark.parametrize(
    "json_data",
    [
        {
            "name": "Test name change",
            "description": "Test description change",
            "full_amount": 2000,
        }
    ],
)
def test_update_project_with_non_exist_id(superuser_client, json_data):
    response = superuser_client.patch(
        os.path.join(URL, "100"),
        json=json_data,
    )
    assert response.status_code == 404, (
        "Запрос с попыткой обновления проекта с несуществующим id должен"
        " возвращать ошибку со статусом 404"
    )


@pytest.mark.usefixtures("charity_project_first")
@pytest.mark.parametrize(
    "json_data, expected_data",
    [
        (
            {"full_amount": 2000},
            {
                "id": 1,
                "name": "Test Charity Project number 1",
                "description": "This is a test charity project number 1",
                "full_amount": 2000,
                "created_date": "2023-01-01T00:00:00",
                "fully_invested": False,
                "invested_amount": 0,
            },
        ),
        (
            {"name": "Testing change project name"},
            {
                "id": 1,
                "name": "Testing change project name",
                "description": "This is a test charity project number 1",
                "full_amount": 1000,
                "created_date": "2023-01-01T00:00:00",
                "fully_invested": False,
                "invested_amount": 0,
            },
        ),
        (
            {"description": "Testing change project description"},
            {
                "id": 1,
                "name": "Test Charity Project number 1",
                "description": "Testing change project description",
                "full_amount": 1000,
                "created_date": "2023-01-01T00:00:00",
                "fully_invested": False,
                "invested_amount": 0,
            },
        ),
    ],
)
def test_update_project(
    superuser_client,
    charity_project_first,
    json_data,
    expected_data,
):
    url = os.path.join(URL, "1")
    response = superuser_client.patch(url, json=json_data)
    assert (
        response.status_code == 200
    ), f"Коректный PATCH-запрос к {url} должен вернуть статус-код 200"
    response_data = response.json()
    missing_keys = EXPECTED_KEYS - response_data.keys()
    assert not missing_keys, (
        f"В ответе на PATCH-запрос к {url} не хвататет следующих ключей:"
        f'`{"`, `".join(missing_keys)}`"'
    )
    response_data.pop("close_date", None)
    assert response_data == expected_data, (
        f"Структура ответа на PATCH-запрос к {url} не соответствует"
        " ожидаемому."
    )


@pytest.mark.usefixtures("charity_project_first")
@pytest.mark.parametrize(
    "json_data",
    [
        {"name": ""},
        {"description": ""},
        {"full_amount": ""},
        {"full_amount": "123abc"},
        {"full_amount": 0.5},
        {"full_amount": 0},
        {"full_amount": -1},
    ],
)
def test_update_project_with_invalid_data(superuser_client, json_data):
    url = os.path.join(URL, "1")
    response = superuser_client.patch(url, json=json_data)
    assert response.status_code == 422, (
        f"Убедитесь что при попытке отправить PATCH-запрос к {url} с"
        "некоректыми данными: постые поля name, description, full_amount"
        "текстовые значения или отрицательные числа или числа с плавоющей"
        "точкой возаращется ответ со статус-кодом 422"
    )


@pytest.mark.usefixtures("charity_project_first")
@pytest.mark.parametrize(
    "json_data",
    [
        {"invested_amount": 500},
        {"fully_invested": True},
        {"close_date": "2023-01-01T00:00:00"},
        {"created_date": "2023-01-01T00:00:00"},
    ],
)
def test_update_project_with_default_filling_fields(
    superuser_client, json_data
):
    url = os.path.join(URL, "1")
    response = superuser_client.patch(url, json=json_data)
    assert response.status_code == 422, (
        f"Убедитесь что при попытке отправить PATCH-запрос к {url} с"
        " полями не предусмотренными спецификацией API для этого эндпоинта"
        "возвращает статус код 422"
    )


def test_delete_project_with_non_exist_id(
    superuser_client, charity_project_first
):
    url = os.path.join(URL, "100")
    response = superuser_client.delete(url)
    assert (
        response.status_code == 404
    ), f"DELETE-запрос к {url} должен возвращать статус-код 404"


@pytest.mark.usefixtures("charity_project_first", "charity_project_second")
def test_delete_project(superuser_client, charity_project_first):
    url = os.path.join(URL, "1")
    response = superuser_client.delete(url)
    assert (
        response.status_code == 204
    ), f"DELETE-запрос к {url} должен возвращать статус-код 204"

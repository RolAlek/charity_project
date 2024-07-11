import os

from test_project import URL as project_url

DONATIONS_URL = "api/donation/"


def test_anonymous_create_project(
    test_client,
    correct_create_testing_data,
):
    response = test_client.post(project_url, json=correct_create_testing_data)
    assert response.status_code == 401, (
        f"POST-запрос к {project_url} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_anonymous_delete_project(test_client):
    url = os.path.join(project_url, "1")
    response = test_client.delete(url)
    assert response.status_code == 401, (
        f"DELETE-запрос к {url} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_anonymous_update_project(test_client, update_testing_data):
    url = os.path.join(project_url, "1")
    response = test_client.patch(
        url,
        json=update_testing_data,
    )
    assert response.status_code == 401, (
        f"PATCH-запрос к {url} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_anonymous_create_donation(test_client):
    response = test_client.post(DONATIONS_URL, json={"full_amount": 1000})
    assert response.status_code == 401, (
        f"POST-запрос к {DONATIONS_URL} анонимного пользователя должен"
        "вернуть 401 статус-код."
    )


def test_anonymous_get_all_donations(test_client):
    response = test_client.get(DONATIONS_URL)
    assert response.status_code == 401, (
        f"GET-запрос к {DONATIONS_URL} анонимного пользователя должен"
        "вернуть 401 статус-код."
    )


def test_get_all_donations_with_regular_user(user_client):
    response = user_client.get(DONATIONS_URL)
    assert response.status_code == 403, (
        f"GET-запрос к {DONATIONS_URL} обычного пользователя должен"
        "вернуть 403 статус-код."
    )


def test_create_project_with_regular_user(
    user_client, correct_create_testing_data
):
    response = user_client.post(project_url, json=correct_create_testing_data)
    assert response.status_code == 403, (
        f"POST-запрос обычного пользователя без root-прав к {project_url} должен"
        f"возвращать статус-код 403"
    )


def test_update_project_with_regular_user(user_client, update_testing_data):
    url = os.path.join(project_url, "1")
    response = user_client.patch(url, json=update_testing_data)
    assert response.status_code == 403, (
        f"PATCH-запрос обычного пользователя без root-прав к {url} должен"
        f"возвращать статус-код 403"
    )


def test_delete_project_with_regular_user(user_client):
    url = os.path.join(project_url, "1")
    response = user_client.delete(url)
    assert response.status_code == 403, (
        f"DELETE-запрос обычного пользователя без root-прав к {url} должен"
        f"возвращать статус-код 403"
    )

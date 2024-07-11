import os

from test_project import URL


def test_create_project_non_superuser(
    test_client,
    correct_create_testing_data,
):
    response = test_client.post(URL, json=correct_create_testing_data)
    assert response.status_code == 401, (
        f"POST-запрос к {URL} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_delete_project_non_superuser(test_client):
    url = os.path.join(URL, "1")
    response = test_client.delete(url)
    assert response.status_code == 401, (
        f"DELETE-запрос к {url} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_update_project_non_superuser(test_client, update_testing_data):
    url = os.path.join(URL, "1")
    response = test_client.patch(
        url,
        json=update_testing_data,
    )
    assert response.status_code == 401, (
        f"PATCH-запрос к {url} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_create_project_with_regular_user(
    user_client, correct_create_testing_data
):
    response = user_client.post(URL, json=correct_create_testing_data)
    assert response.status_code == 403, (
        f"POST-запрос обычного пользователя без root-прав к {URL} должен"
        f"возвращать статус-код 403"
    )


def test_update_project_with_regular_user(user_client, update_testing_data):
    url = os.path.join(URL, "1")
    response = user_client.patch(url, json=update_testing_data)
    assert response.status_code == 403, (
        f"PATCH-запрос обычного пользователя без root-прав к {url} должен"
        f"возвращать статус-код 403"
    )


def test_delete_project_with_regular_user(user_client):
    url = os.path.join(URL, "1")
    response = user_client.delete(url)
    assert response.status_code == 403, (
        f"DELETE-запрос обычного пользователя без root-прав к {url} должен"
        f"возвращать статус-код 403"
    )

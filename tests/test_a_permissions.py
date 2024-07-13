from tests.conftest import PROJECT_URL, PROJECT_DETAIL, DONATION_URL


def test_anonymous_create_project(
    test_client,
    correct_create_testing_data,
):
    response = test_client.post(PROJECT_URL, json=correct_create_testing_data)
    assert response.status_code == 401, (
        f"POST-запрос к {PROJECT_URL} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_anonymous_delete_project(test_client):
    response = test_client.delete(PROJECT_DETAIL)
    assert response.status_code == 401, (
        f"DELETE-запрос к {PROJECT_DETAIL} анонимного пользователя должен"
        " вернуть статус-код 401."
    )


def test_anonymous_update_project(test_client, update_testing_data):
    response = test_client.patch(
        PROJECT_DETAIL,
        json=update_testing_data,
    )
    assert response.status_code == 401, (
        f"PATCH-запрос к {PROJECT_DETAIL} анонимного пользователя должен вернуть"
        " статус-код 401."
    )


def test_anonymous_create_donation(test_client):
    response = test_client.post(DONATION_URL, json={"full_amount": 1000})
    assert response.status_code == 401, (
        f"POST-запрос к {DONATION_URL} анонимного пользователя должен"
        "вернуть 401 статус-код."
    )


def test_anonymous_get_all_donations(test_client):
    response = test_client.get(DONATION_URL)
    assert response.status_code == 401, (
        f"GET-запрос к {DONATION_URL} анонимного пользователя должен"
        "вернуть 401 статус-код."
    )


def test_get_all_donations_with_regular_user(user_client):
    response = user_client.get(DONATION_URL)
    assert response.status_code == 403, (
        f"GET-запрос к {DONATION_URL} обычного пользователя должен"
        "вернуть 403 статус-код."
    )


def test_create_project_with_regular_user(
    user_client, correct_create_testing_data
):
    response = user_client.post(PROJECT_URL, json=correct_create_testing_data)
    assert response.status_code == 403, (
        f"POST-запрос обычного пользователя без root-прав к {PROJECT_URL}"
        f"должен возвращать статус-код 403"
    )


def test_update_project_with_regular_user(user_client, update_testing_data):
    response = user_client.patch(PROJECT_DETAIL, json=update_testing_data)
    assert response.status_code == 403, (
        f"PATCH-запрос обычного пользователя без root-прав к {PROJECT_DETAIL}"
        "должен возвращать статус-код 403"
    )


def test_delete_project_with_regular_user(user_client):
    response = user_client.delete(PROJECT_DETAIL)
    assert response.status_code == 403, (
        f"DELETE-запрос обычного пользователя без root-прав к {PROJECT_DETAIL}"
        "должен возвращать статус-код 403"
    )

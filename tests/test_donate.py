import pytest

from tests.conftest import DONATION_URL

EXPECTED_KEYS_FOR_USER = {
    "full_amount",
    "id",
    "created_date",
}


@pytest.mark.parametrize(
    "invalid_amount",
    [
        0,
        -1,
        0.5,
        "string",
        None,
        "null",
        "",
    ],
)
def test_invalid_amount(invalid_amount, user_client):
    response = user_client.post(
        DONATION_URL,
        json={"full_amount": invalid_amount},
    )
    assert response.status_code == 422, (
        f"POST-запрос к {DONATION_URL} с full_amount == {invalid_amount}"
        "должен вернуть 422 статус-код."
    )


def test_create_donation(user_client):
    response = user_client.post(
        DONATION_URL,
        json={"full_amount": 100},
    )
    assert response.status_code == 201, (
        f"POST-запрос к {DONATION_URL} с full_amount == 100 должен вернуть"
        "201 статус-код."
    )
    data = response.json()
    missing_keys = EXPECTED_KEYS_FOR_USER - data.keys()
    assert not missing_keys, (
        f"При коректном POST-запросе к {DONATION_URL} в ответе не"
        f"хватает следующих ключей: `{"`, `".join(missing_keys)}`"
    )


@pytest.mark.usefixtures("donation")
def test_get_all_donations_for_admin(superuser_client):
    response = superuser_client.get(DONATION_URL)
    assert (
        response.status_code == 200
    ), f"GET-запрос root'a к {DONATION_URL} должен вернуть 200 статус-код."
    data = response.json()
    assert isinstance(
        data, list
    ), f"GET-запрос root'a к {DONATION_URL} должен вернуть список."
    assert data[0] == {
        "full_amount": 1000,
        "id": 1,
        "created_date": "2023-01-01T00:00:00",
        "user_id": 1,
        "invested_amount": 0,
        "fully_invested": False,
    }

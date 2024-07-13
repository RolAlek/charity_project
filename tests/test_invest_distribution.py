import pytest

from tests.conftest import DONATION_URL, PROJECT_URL


@pytest.mark.usefixtures("charity_project_first", "charity_project_second")
def test_donation_fully_invested_amount_for_two_projects(
    user_client,
    charity_project_first,
    charity_project_second,
):
    common_asser_msg = (
        "При тестировании создано два пустых проекта. "
        "Затем тест создал два пожертвования, которые "
        "полностью и без остатка покрывают требуемую сумму первого проекта. "
        "Второй проект должен оставаться не инвестированным."
    )
    [
        user_client.post(DONATION_URL, json={"full_amount": 500})
        for _ in range(2)
    ]
    first_project, second_project = user_client.get(PROJECT_URL).json()
    assert first_project["fully_invested"], common_asser_msg
    assert not second_project["fully_invested"], common_asser_msg
    assert second_project["invested_amount"] == 0, common_asser_msg


def test_donation_to_little_invest_project(
    user_client,
    charity_project_little_invested,
    charity_project_second,
):
    common_asser_msg = (
        "При тестировании создано два проекта, "
        "один из которых частично инвестирован, а второй - без инвестиций. "
        "Затем тест создает пожертвование, недостаточное для закрытия "
        "первого проекта. Пожертвование должно добавиться "
        "в первый проект; второй проект должен остаться пустым."
    )
    user_client.post(DONATION_URL, json={"full_amount": 1000})
    first_project, second_project = user_client.get(PROJECT_URL).json()
    print(first_project, second_project)
    assert not first_project["fully_invested"], common_asser_msg
    assert (
        first_project["invested_amount"] == 2000
    ), common_asser_msg
    assert not second_project["fully_invested"], common_asser_msg
    assert second_project["invested_amount"] == 0, common_asser_msg

from datetime import datetime
from string import ascii_uppercase

from aiogoogle import Aiogoogle
from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
SHEET_BODY = {
    "properties": {
        "sheetType": "GRID",
        "sheetId": 0,
        "title": "Лист1",
        "gridProperties": {"rowCount": 100, "columnCount": 11},
    }
}
TABLE_HEADER = [
    ["Отчет от"],
    ["Топ проектов по скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"],
]


async def create_spreadsheet(wrapp_service: Aiogoogle):
    service = await wrapp_service.discover("sheets", "v4")
    response = await wrapp_service.as_service_account(
        service.spreadsheets.create(
            json={
                "properties": {
                    "title": f"Отчет от {datetime.now().strftime(FORMAT)}",
                    "locale": "ru_RU",
                },
                "sheets": [SHEET_BODY],
            }
        )
    )
    return response["spreadsheetId"]


async def set_user_permissions(
    wrapp_service: Aiogoogle,
    spreadsheet_id: str,
) -> None:
    service = await wrapp_service.discover("drive", "v3")
    await wrapp_service.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json={
                "type": "user",
                "role": "writer",
                "emailAddress": settings.google.email,
            },
            fields="id",
        ),
    )


async def spreadsheet_update_values(
    spreadsheet_id: str,
    projects: list,
    wrapp_service: Aiogoogle,
) -> None:
    service = await wrapp_service.discover("sheets", "v4")
    table_values = TABLE_HEADER.copy()
    table_values[0].append(datetime.now().strftime(FORMAT))

    for project in projects:
        table_values.append([*project.values()])

    column = ascii_uppercase[len(max(table_values, key=len)) - 1]
    lines_number = len(table_values)
    await wrapp_service.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f"A1:{column}{lines_number}",
            valueInputOption="USER_ENTERED",
            json={"majorDimension": "ROWS", "values": table_values},
        )
    )

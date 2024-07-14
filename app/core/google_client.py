from aiogoogle import Aiogoogle
from aiogoogle.auth.creds import ServiceAccountCreds

from core.config import settings

INFO = {
    "type": settings.google.type,
    "project_id": settings.google.project_id,
    "private_key_id": settings.google.private_key_id,
    "private_key": settings.google.private_key.replace(r"\n", "\n"),
    "client_email": settings.google.client_email,
    "client_id": settings.google.client_id,
    "auth_uri": settings.google.auth_uri,
    "token_uri": settings.google.token_uri,
    "auth_provider_x509_cert_url": settings.google.auth_provider_x509_cert_url,
    "client_x509_cert_url": settings.google.client_x509_cert_url,
}

credentials = ServiceAccountCreds(
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ],
    **INFO,
)


async def get_google_client():
    async with Aiogoogle(service_account_creds=credentials) as google:
        return google

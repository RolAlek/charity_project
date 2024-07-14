from pydantic import BaseModel, EmailStr, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    url: PostgresDsn


class GoogleAPISettings(BaseSettings):
    type: str | None = None
    project_id: str | None = None
    private_key_id: str | None = None
    private_key: str | None = None
    client_email: str | None = None
    client_id: str | None = None
    auth_uri: str | None = None
    token_uri: str | None = None
    auth_provider_x509_cert_url: str | None = None
    client_x509_cert_url: str | None = None
    email: str | None = None


class RootData(BaseModel):
    login: EmailStr
    password: str
    first_name: str
    last_name: str
    birthday: str


class UserSettings(BaseModel):
    secret: str
    lifetime: int = 3600
    init_root: bool = False
    root: RootData


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="APP__",
        extra="allow",
        case_sensitive=False,
    )

    app_title: str = "Charity Project Application"
    db: DatabaseSettings
    user: UserSettings
    google: GoogleAPISettings


settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    app_name: str = "FileService"
    SQLALCHEMY_DATABASE_URL: str


settings = Settings()

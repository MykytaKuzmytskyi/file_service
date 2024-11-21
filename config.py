from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="allow")

    app_name: str = "FileSharingAPI"
    USER_SECRET_KEY: str
    SQLALCHEMY_DATABASE_URL: str


settings = Settings()

if __name__ == '__main__':
    print(settings.SQLALCHEMY_DATABASE_URL)

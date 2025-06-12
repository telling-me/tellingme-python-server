import os
from enum import StrEnum
from zoneinfo import ZoneInfo

from pydantic_settings import BaseSettings


class Env(StrEnum):
    LOCAL = "local"
    STAGE = "stage"
    PROD = "prod"


class Settings(BaseSettings):
    ENV: Env = Env.LOCAL
    DB_HOST: str = "localhost"
    DB_PORT: int = 3307
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "tellingme_local"
    DB_TIMEZONE: str = "Asia/Seoul"
    DB_CHARSET: str = "utf8mb4"
    APPLE_URL: str = "https://sandbox.itunes.apple.com/verifyReceipt"
    APPLE_SHARED_SECRET: str = "YOUR_SHARED_SECRET"

    class Config:
        env_file = f".env.{os.getenv('ENV', 'local')}"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return f"mysql+asyncmy://{self.DB_USER}:{self.DB_PASSWORD}" f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def db_zoneinfo(self) -> ZoneInfo:
        return ZoneInfo(self.DB_TIMEZONE)

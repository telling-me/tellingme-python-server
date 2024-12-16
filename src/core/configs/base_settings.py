import os
from enum import StrEnum

from pydantic_settings import BaseSettings


class Env(StrEnum):
    LOCAL = "local"
    STAGE = "stage"
    PROD = "prod"


class Settings(BaseSettings):
    ENV: Env = Env.LOCAL
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "database_name"
    DB_TIMEZONE: str = "Asia/Seoul"
    DB_CHARSET: str = "utf8mb4"
    APPLE_URL: str = "https://sandbox.itunes.apple.com/verifyReceipt"
    APPLE_SHARED_SECRET: str = "YOUR_SHARED_SECRET"

    class Config:
        env_file = f".env.{os.getenv('ENV', 'local')}"
        env_file_encoding = "utf-8"

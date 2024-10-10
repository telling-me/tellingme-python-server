from pydantic_settings import BaseSettings
from enum import StrEnum


class Env(StrEnum):
    LOCAL = "local"
    STAGE = "stage"
    PROD = "prod"


class Settings(BaseSettings):
    ENV: Env = Env.LOCAL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_TIMEZONE: str = "Asia/Seoul"
    DB_CHARSET: str = "utf8mb4"

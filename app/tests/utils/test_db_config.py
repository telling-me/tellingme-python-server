from typing import Any

from tortoise.backends.base.config_generator import generate_config

from app.core.configs import settings
from app.core.database.tortoise_database_settings import TORTOISE_APP_MODELS

TEST_BASE_URL = "http://test"
TEST_DB_LABEL = "models"
TEST_DB_TZ = "Asia/Seoul"


def get_test_db_config() -> dict[Any, Any]:
    config = generate_config(
        db_url=f"mysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/test",
        app_modules={TEST_DB_LABEL: TORTOISE_APP_MODELS},
        connection_label=TEST_DB_LABEL,
        testing=True,
    )
    config["timezone"] = TEST_DB_TZ
    return config

from typing import Any, AsyncGenerator
from unittest.mock import Mock, patch

import httpx
import pytest
from _pytest.fixtures import FixtureRequest
from tortoise import Tortoise
from tortoise.backends.base.config_generator import generate_config
from tortoise.contrib.test import finalizer, initializer

from app import app
from app.core.configs import settings
from app.core.database.tortoise_database_settings import TORTOISE_APP_MODELS
from app.tests.telling_me_client import TellingMeClient

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


@pytest.fixture(scope="session", autouse=True)
def initialize(request: FixtureRequest) -> None:
    with patch("tortoise.contrib.test.getDBConfig", Mock(return_value=get_test_db_config())):
        initializer(modules=TORTOISE_APP_MODELS, loop=None)
    request.addfinalizer(finalizer)


@pytest.fixture()
async def init_tortoise_connection() -> AsyncGenerator[None, None]:
    """
    tortoise orm 테스트 시 initializer에서는 테이블 생성 후 connection을 전부 삭제한다.
    Tortoise.get_connection("default") or atomic()을 사용 시 연결을 찾을 수 없어 에러 발생
    이런 오류를 해결하기 위해서 직접 connection을 생성
    """
    await Tortoise.init(
        db_url=f"mysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/test",
        modules={"models": TORTOISE_APP_MODELS},
    )
    yield
    await Tortoise.close_connections()


@pytest.fixture()
async def telling_me_client() -> AsyncGenerator[TellingMeClient, None]:
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=TEST_BASE_URL) as client:
        yield TellingMeClient(client)

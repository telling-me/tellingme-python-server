import asyncio
import logging

from celery import Celery
from tortoise import Tortoise, Model, fields

from celery_models import Question
from core.configs import settings


TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
            "credentials": {
                "host": settings.DB_HOST,
                "port": settings.DB_PORT,
                "user": settings.DB_USER,
                "password": settings.DB_PASSWORD,
                "database": settings.DB_NAME,
                "connect_timeout": 5,
                "charset": settings.DB_CHARSET,
                "minsize": 5,  # 커넥션 풀 최소 크기
                "maxsize": 10,  # 커넥션 풀 최대 크기
            },
        },
    },
    "apps": {
        "models": {
            "models": ["app.celery_models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,  # 비동기 ORM에서 타임존 설정을 고려하지 않는다면 False
    "timezone": settings.DB_TIMEZONE,  # 타임존 설정
}

celery_app = Celery(
    "telling-me-celery",
    broker="redis://localhost:6379/0",  # Redis를 브로커로 사용
    backend="redis://localhost:6379/0",  # Redis를 결과 백엔드로 사용
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Seoul",
    enable_utc=True,
    result_expires=3600,  # 작업 결과 만료 시간 (초 단위)
)


@celery_app.task(name="daily_task")
def daily_task() -> None:
    asyncio.run(execute_async_daily_task())


async def execute_async_daily_task() -> None:
    await initialize_celery()
    try:
        print("Executing daily task!")
        await Question.create(
            date="2023-07-29",
            title="Title for 2024-12-10",
            phrase="Phrase",
            spare_phrase="s",
            spare_title="s",
        )

    finally:
        await close_celery_connections()


async def initialize_celery():
    logger = logging.getLogger(__name__)
    logger.info(f"Current path: 여기")
    await Tortoise.init(config=TORTOISE_ORM)


async def close_celery_connections():
    await Tortoise.close_connections()


if __name__ == "__main__":
    celery_app.start()

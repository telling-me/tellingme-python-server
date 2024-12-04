import asyncio
import logging

from celery import Celery
from tortoise import Tortoise

from common.tasks.mission_task import mission_reset_task
from common.tasks.renew_subscription_task import renew_subscription_task
from core.database.database_settings import TORTOISE_ORM

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
        await mission_reset_task()
        await renew_subscription_task()
    finally:
        await close_celery_connections()


async def initialize_celery():
    logger = logging.getLogger(__name__)
    logger.info(f"Current path: 여기")
    logging.basicConfig(level=logging.DEBUG)
    db_client_logger = logging.getLogger("tortoise.db_client")
    db_client_logger.setLevel(logging.DEBUG)

    await Tortoise.init(config=TORTOISE_ORM)


async def close_celery_connections():
    await Tortoise.close_connections()


if __name__ == "__main__":
    celery_app.start()

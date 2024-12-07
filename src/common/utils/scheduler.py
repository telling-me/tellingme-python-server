import logging

from apscheduler.jobstores.redis import RedisJobStore  # type: ignore
from apscheduler.schedulers.background import BackgroundScheduler  # type: ignore

from core.configs.celery_settings import celery_app

logger = logging.getLogger(__name__)


def execute_daily_task() -> None:
    celery_app.send_task("daily_task")


def start_scheduler() -> None:
    scheduler = BackgroundScheduler(
        jobstores={"default": RedisJobStore(host="localhost", port=6379, db=0)},
        timezone="Asia/Seoul",
    )
    scheduler.start()
    logger.info("Scheduler started")

    scheduler.add_job(
        func=execute_daily_task,
        trigger="cron",
        hour=00,
        minute=28,
        id="daily_task",
        replace_existing=True,
    )

from fastapi import FastAPI

from app.common.handlers.exception_handler import attach_exception_handlers
from app.common.handlers.router_handler import attach_router_handlers
from app.common.utils.scheduler import start_scheduler
from app.core.database.tortoise_database_settings import database_initialize


def post_construct(app: FastAPI) -> None:
    attach_router_handlers(app)
    attach_exception_handlers(app)
    database_initialize(app)
    start_scheduler()

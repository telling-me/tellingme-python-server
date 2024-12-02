from fastapi import FastAPI

from core.tasks.scheduler import start_scheduler
from common.handlers.exception_handler import attach_exception_handlers
from common.handlers.router_handler import attach_router_handlers
from core.database.database_settings import database_initialize


def post_construct(app: FastAPI) -> None:
    attach_router_handlers(app)
    attach_exception_handlers(app)
    database_initialize(app)
    start_scheduler()

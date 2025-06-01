from fastapi import FastAPI
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise

from app.core.configs import settings

TORTOISE_APP_MODELS = [
    "app.apis.v2.questions.models.question",
    "app.apis.v2.users.models.user",
    "app.apis.v2.users.models.refresh_token",
    "app.apis.v2.badges.models.badge",
    "app.apis.v2.colors.models.color",
    "app.apis.v2.answers.models.answer",
    "app.apis.v2.teller_cards.models.teller_card",
    "app.apis.v2.levels.models.level",
    "app.apis.v2.cheese_managers.models.cheese_manager",
    "app.apis.v2.items.models.item",
    "app.apis.v2.missions.models.mission",
    "app.apis.v2.likes.models.like",
    "app.apis.v2.emotions.models.emotion",
    "app.apis.v2.purchases.models.purchase_history",
]

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
            "models": TORTOISE_APP_MODELS,
            "default_connection": "default",
        },
    },
    "use_tz": False,  # 비동기 ORM에서 타임존 설정을 고려하지 않는다면 False
    "timezone": settings.DB_TIMEZONE,  # 타임존 설정
}


def database_initialize(app: FastAPI) -> None:
    Tortoise.init_models(TORTOISE_APP_MODELS, "models")
    register_tortoise(
        app,
        config=TORTOISE_ORM,
        generate_schemas=False,
        add_exception_handlers=True,
    )

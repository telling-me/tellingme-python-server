from fastapi import FastAPI

from app.apis.v2.badge_router import badge_router as badge_router
from app.apis.v2.cheese_router import cheese_router as cheese_router
from app.apis.v2.color_router import color_router as color_router
from app.apis.v2.emotion_router import emotion_router as emotion_router
from app.apis.v2.mission_router import mission_router as mission_router
from app.apis.v2.mobile_router import mobile_router as mobile_router
from app.apis.v2.payment_router import payment_router as payment_router
from app.apis.v2.teller_card_router import teller_card_router as teller_card_router


def attach_router_handlers(app: FastAPI) -> None:
    app.include_router(router=mobile_router, prefix="/api/v2")
    app.include_router(router=badge_router, prefix="/api/v2")
    app.include_router(router=color_router, prefix="/api/v2")
    app.include_router(router=teller_card_router, prefix="/api/v2")
    app.include_router(router=payment_router, prefix="/api/v2")
    app.include_router(router=mission_router, prefix="/api/v2")
    app.include_router(router=cheese_router, prefix="/api/v2")
    app.include_router(router=emotion_router, prefix="/api/v2")

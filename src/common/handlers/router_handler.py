from app.v2.mobiles.router import router as mobile_router
from app.v2.questions.router import router as question_router
from app.v2.badges.router import router as badge_router
from app.v2.teller_cards.router import router as teller_card_router
from app.v2.payments.router import router as payment_router
from app.v2.purchases.router import router as purchase_router
from app.v2.missions.router import router as mission_router
from app.v2.answers.router import router as answer_router
from app.v2.cheese_managers.router import router as cheese_router


def attach_router_handlers(app):
    app.include_router(router=mobile_router, prefix="/api/v2")
    app.include_router(router=badge_router, prefix="/api/v2")
    app.include_router(router=question_router, prefix="/api/v2")
    app.include_router(router=teller_card_router, prefix="/api/v2")
    app.include_router(router=payment_router, prefix="/api/v2")
    app.include_router(router=purchase_router, prefix="/api/v2")
    app.include_router(router=mission_router, prefix="/api/v2")
    app.include_router(router=cheese_router, prefix="/api/v2")
    app.include_router(router=answer_router, prefix="/test")

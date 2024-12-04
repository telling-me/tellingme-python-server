from app.v2.purchases.services.purchase_service import PurchaseService


async def renew_subscription_task() -> None:
    purchase_service = PurchaseService()
    await purchase_service.renew_subscription()

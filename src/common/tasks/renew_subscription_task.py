from app.v2.purchases.services.purchase_service import PurchaseService


async def renew_subscription_task() -> None:
    purchase_service = PurchaseService()
    await purchase_service.process_subscriptions_renewal()


async def expire_subscription_task() -> None:
    purchase_service = PurchaseService()
    await purchase_service.expire_subscriptions()

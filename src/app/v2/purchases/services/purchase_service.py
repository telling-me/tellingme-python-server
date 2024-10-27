from app.v2.items.models.item import ProductInventory, ItemInventory
from app.v2.users.services.user_service import UserService


class PurchaseService:
    @staticmethod
    async def process_krw_payment(product: ProductInventory, quantity: int):
        print(f"Processing KRW payment: {product.price * quantity} KRW")
        # 여기에 실제 KRW 결제 처리 로직 구현

    @staticmethod
    async def process_subscription(
        item: ItemInventory, quantity: int, measurement: str
    ):
        print(f"Activating subscription: {item.item_code} for {quantity} {measurement}")
        # 구독 활성화 로직 구현

    @staticmethod
    async def add_points(user_id: str, quantity: int):
        print(f"Adding {quantity} points to user's balance")
        await UserService.add_points(user_id, quantity)

    @staticmethod
    async def add_cheese(user_id: str, quantity: int):
        print(f"Adding {quantity} cheese to user's balance")
        await UserService.add_cheese(user_id, quantity)

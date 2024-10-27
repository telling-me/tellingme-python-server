from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from app.v2.badges.services.badge_service import BadgeService
from app.v2.cheese_managers.models.cheese_manager import CheeseManager
from app.v2.colors.services.color_service import ColorService
from app.v2.emotions.services.emotion_service import EmotionService
from app.v2.items.models.item import (
    ItemInventory,
    ProductInventory,
    ItemInventoryProductInventory,
)
from app.v2.users.services.user_service import UserService


class PaymentService:
    @staticmethod
    async def validate_payment(product_code: str):
        try:
            product = await ProductInventory.get(product_code=product_code)

            if product.transaction_currency != "CHEESE":
                raise HTTPException(
                    status_code=400, detail="Invalid transaction currency for payment."
                )

            item_inventory_products = await ItemInventoryProductInventory.filter(
                product_inventory_id=product.product_id
            ).all()

            if not item_inventory_products:
                raise HTTPException(
                    status_code=404, detail="No inventory found for this product."
                )

            return product, item_inventory_products

        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Product not found.")

    @classmethod
    @atomic()
    async def process_cheese_payment(
        cls,
        product: ProductInventory,
        item_inventory_products: list[ItemInventoryProductInventory],
        user_id: str,
        cheese_manager_id: str,
    ):
        total_cheese = await CheeseManager.get_total_cheese_amount_by_manager(
            cheese_manager_id=cheese_manager_id
        )

        total_required_cheese = product.price

        if total_cheese < total_required_cheese:
            raise HTTPException(
                status_code=400, detail="Not enough cheese for this purchase"
            )

        try:
            await CheeseManager.use_cheese(cheese_manager_id, total_required_cheese)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        for item_inventory_product in item_inventory_products:
            item: ItemInventory = await item_inventory_product.item_inventory
            quantity = item_inventory_product.quantity

            if item.item_category == "BADGE":
                for _ in range(quantity):
                    await BadgeService.add_badge(
                        user_id=user_id, badge_code=item.item_code
                    )
            elif item.item_category == "COLOR":
                for _ in range(quantity):
                    await ColorService.add_color(
                        user_id=user_id, color_code=item.item_code
                    )
            elif item.item_category == "EMOTION":
                for _ in range(quantity):
                    await EmotionService.add_emotion(
                        user_id=user_id, emotion_code=item.item_code
                    )
            else:
                raise ValueError(
                    f"Invalid item category for cheese payment: {item.item_category}"
                )

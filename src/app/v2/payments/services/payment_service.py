from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.transactions import atomic

from app.v2.badges.services.badge_service import BadgeService
from app.v2.cheese_managers.models.cheese_manager import CheeseManager
from app.v2.colors.services.color_service import ColorService
from app.v2.emotions.services.emotion_service import EmotionService
from app.v2.items.models.item import ItemInventory, ItemInventoryProductInventory, ProductInventory
from common.exceptions.custom_exception import CustomException
from common.exceptions.error_code import ErrorCode


class PaymentService:
    @staticmethod
    async def validate_payment(
        product_code: str,
    ) -> tuple[ProductInventory, list[ItemInventoryProductInventory]]:
        try:
            product = await ProductInventory.get(product_code=product_code)

            if product.transaction_currency != "CHEESE":
                raise CustomException(ErrorCode.INVALID_TRANSACTION_CURRENCY)

            item_inventory_products = await ItemInventoryProductInventory.filter(
                product_inventory_id=product.product_id
            ).all()

            if not item_inventory_products:
                raise CustomException(ErrorCode.NO_INVENTORY_FOR_PRODUCT)

            return product, item_inventory_products

        except DoesNotExist:
            raise CustomException(ErrorCode.PRODUCT_NOT_FOUND)

    @classmethod
    @atomic()
    async def process_cheese_payment(
        cls,
        product: ProductInventory,
        item_inventory_products: list[ItemInventoryProductInventory],
        user_id: str,
        cheese_manager_id: int,
    ) -> None:
        total_cheese = await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=cheese_manager_id)

        total_required_cheese = product.price

        if total_cheese < total_required_cheese:
            raise CustomException(ErrorCode.NOT_ENOUGH_CHEESE)

        try:
            await CheeseManager.use_cheese(cheese_manager_id, int(total_required_cheese))
        except ValueError as e:
            raise CustomException(ErrorCode.NOT_ENOUGH_CHEESE)

        try:
            for item_inventory_product in item_inventory_products:
                item: ItemInventory = await item_inventory_product.item_inventory
                quantity = item_inventory_product.quantity

                if item.item_category == "BADGE":
                    for _ in range(quantity):
                        await BadgeService.add_badge(user_id=user_id, badge_code=item.item_code)
                elif item.item_category == "COLOR":
                    for _ in range(quantity):
                        await ColorService.add_color(user_id=user_id, color_code=item.item_code)
                elif item.item_category == "EMOTION":
                    for _ in range(quantity):
                        await EmotionService.add_emotion(user_id=user_id, emotion_code=item.item_code)
                else:
                    raise CustomException(ErrorCode.INVALID_ITEM_CATEGORY)
        except IntegrityError:
            raise CustomException(ErrorCode.DUPLICATE_PURCHASE)

from tortoise.exceptions import DoesNotExist, IntegrityError
from tortoise.transactions import atomic

from app.common.constants.item_category import ItemCategory
from app.common.exceptions.custom_exception import CustomException
from app.common.exceptions.error_code import ErrorCode
from app.models.badge import Badge
from app.models.cheese_manager import CheeseManager
from app.models.color import Color
from app.models.emotion import Emotion
from app.models.item import ItemInventory, ItemInventoryProductInventory, ProductInventory
from app.models.user import User
from app.services.badge_service import BadgeService
from app.services.color_service import ColorService
from app.services.emotion_service import EmotionService


class PaymentService:
    @staticmethod
    async def _validate_payment(
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
        product_code: str,
        user_id: str,
    ) -> str:
        # 1. 제품 코드 검증
        product, item_inventory_products = await cls._validate_payment(product_code)

        # 2. 유저 정보 조회 및 치즈 잔액 조회
        user = await User.get_user_info_by_user_id(user_id=user_id)
        total_cheese = await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=user.cheese_manager_id)

        # 3. 치즈 결제 진행
        total_required_cheese = product.price

        if total_cheese < total_required_cheese:
            raise CustomException(ErrorCode.NOT_ENOUGH_CHEESE)

        await CheeseManager.use_cheese(user.cheese_manager_id, int(total_required_cheese))

        # 4. 아이템 부여
        try:
            for item_inventory_product in item_inventory_products:
                item: ItemInventory = await item_inventory_product.item_inventory
                quantity = item_inventory_product.quantity

                if item.item_category == ItemCategory.BADGE:
                    for _ in range(quantity):
                        await Badge.create_by_user_id(user_id=user_id, badge_code=item.item_code)
                elif item.item_category == ItemCategory.COLOR:
                    for _ in range(quantity):
                        await Color.create_by_user_id(user_id=user_id, color_code=item.item_code)
                elif item.item_category == ItemCategory.EMOTION:
                    for _ in range(quantity):
                        await Emotion.create_by_user_id(user_id=user_id, emotion_code=item.item_code)
                else:
                    raise CustomException(ErrorCode.INVALID_ITEM_CATEGORY)

            return product_code
        except IntegrityError:
            raise CustomException(ErrorCode.DUPLICATE_PURCHASE)

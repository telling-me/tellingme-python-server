from typing import Any, cast

import httpx
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from app.v2.items.models.item import ItemInventory, ItemInventoryProductInventory, ProductInventory
from app.v2.purchases.models.purchase_history import PurchaseHistory, Subscription
from app.v2.purchases.models.purchase_status import PurchaseStatus, SubscriptionStatus, purchase_mapping
from app.v2.users.services.user_service import UserService
from core.configs import settings


class PurchaseService:
    @atomic()
    async def process_apple_purchase(self, receipt_data: str, user_id: str) -> None:
        response = await self._validate_apple_receipt(receipt_data=receipt_data)

        latest_receipt_info = self._extract_latest_receipt_info(response)
        transaction_id = latest_receipt_info["transaction_id"]
        original_transaction_id = latest_receipt_info["original_transaction_id"]
        expires_date_ms = int(latest_receipt_info.get("expires_date_ms", 0))
        purchase_date_ms = int(latest_receipt_info.get("purchase_date_ms", 0))
        product_code = purchase_mapping.get(latest_receipt_info["product_id"], latest_receipt_info["product_id"])

        await self._create_or_update_subscription(
            user_id=user_id,
            product_code=product_code,
            transaction_id=transaction_id,
            expires_date_ms=expires_date_ms,
        )

        subscription = await self._get_subscription(user_id, product_code)

        if subscription is None:
            raise DoesNotExist("Subscription not found")

        await self._create_purchase_history(
            user_id=user_id,
            subscription=subscription,
            product_code=product_code,
            transaction_id=transaction_id,
            original_transaction_id=original_transaction_id,
            expires_date_ms=expires_date_ms,
            purchase_date_ms=purchase_date_ms,
            quantity=int(latest_receipt_info.get("quantity", 1)),
        )

        item_inventory_products = await self._validate_purchase(product_code=product_code)

        await self._process_purchase(user_id=user_id, item_inventory_products=item_inventory_products)

    @staticmethod
    def _extract_latest_receipt_info(response: dict) -> dict:
        return response.get("latest_receipt_info", [])[0]

    @staticmethod
    async def _validate_apple_receipt(receipt_data: str) -> dict[str, Any]:

        url = settings.APPLE_URL

        payload = {
            "receipt-data": receipt_data,
            "password": settings.APPLE_SHARED_SECRET,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
        if response.status_code == 200:
            return cast(dict[str, Any], response.json())
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to Apple server")

    @staticmethod
    async def _create_or_update_subscription(
        user_id: str, product_code: str, transaction_id: str, expires_date_ms: int
    ) -> None:
        await Subscription.create_or_update_subscription(
            user_id=user_id,
            product_code=product_code,
            transaction_id=transaction_id,
            expires_date_ms=expires_date_ms,
            status=SubscriptionStatus.ACTIVE,
        )

    @staticmethod
    async def _get_subscription(user_id: str, product_code: str) -> Subscription | None:
        return await Subscription.get_subscription_by_user_id_and_product_code(
            user_id=user_id, product_code=product_code
        )

    @staticmethod
    async def _create_purchase_history(
        user_id: str,
        subscription: Subscription,
        product_code: str,
        transaction_id: str,
        original_transaction_id: str,
        expires_date_ms: int,
        purchase_date_ms: int,
        quantity: int,
    ) -> None:
        await PurchaseHistory.create_purchase_history(
            user_id=user_id,
            subscription_id=subscription.subscription_id if subscription else None,
            product_code=product_code,
            transaction_id=transaction_id,
            original_transaction_id=original_transaction_id,
            status=PurchaseStatus.AVAILABLE,
            expires_date_ms=expires_date_ms,
            purchase_date_ms=purchase_date_ms,
            quantity=quantity,
            is_refunded=False,
            refunded_at=None,
        )

    @staticmethod
    async def _validate_purchase(
        product_code: str,
    ) -> list[ItemInventoryProductInventory]:
        try:
            product = await ProductInventory.get(product_code=product_code)

            if product.transaction_currency not in ["KRW", "CHEESE"]:
                raise HTTPException(status_code=400, detail="Invalid transaction currency for purchase.")

            item_inventory_products = await ItemInventoryProductInventory.filter(
                product_inventory_id=product.product_id
            ).all()

            if not item_inventory_products:
                raise HTTPException(status_code=404, detail="No inventory found for this product.")
            return item_inventory_products
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Product not found.")

    @classmethod
    async def _process_purchase(
        cls,
        item_inventory_products: list[ItemInventoryProductInventory],
        user_id: str,
        # cheese_manager_id: int,
    ) -> None:
        for item_inventory_product in item_inventory_products:
            item: ItemInventory = await item_inventory_product.item_inventory
            quantity = item_inventory_product.quantity

            if item.item_category == "SUBSCRIPTION":
                await UserService.set_is_premium(user_id=user_id, is_premium=True)
            # elif item.item_category == "CHEESE":
            #     await CheeseService.add_cheese(cheese_manager_id=cheese_manager_id, amount=quantity)
            else:
                raise ValueError(f"Invalid item category for purchase: {item.item_category}")

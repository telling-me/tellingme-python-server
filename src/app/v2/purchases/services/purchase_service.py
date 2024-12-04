import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, cast

import httpx
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from app.v2.items.models.item import ItemInventory, ItemInventoryProductInventory, ProductInventory
from app.v2.purchases.dtos.purchase_dto import ReceiptInfoDTO
from app.v2.purchases.models.purchase_history import PurchaseHistory, Subscription
from app.v2.purchases.models.purchase_status import PurchaseStatus, SubscriptionStatus, purchase_mapping
from app.v2.users.services.user_service import UserService
from core.configs import settings


class PurchaseService:
    @atomic()
    async def process_apple_purchase(self, receipt_data: str, user_id: str) -> None:
        response = await self._validate_apple_receipt(receipt_data=receipt_data)

        latest_receipt_info = self._extract_latest_receipt_info(response)

        if latest_receipt_info is None:
            raise ValueError("No valid receipt information found.")

        receipt_info = await self._parse_receipt_info(latest_receipt_info)

        await self._create_or_update_subscription(
            user_id=user_id,
            product_code=receipt_info.product_code,
            transaction_id=receipt_info.transaction_id,
            expires_date_ms=receipt_info.expires_date_ms,
        )

        subscription = await self._get_subscription(user_id, receipt_info.product_code)

        if subscription is None:
            raise DoesNotExist("Subscription not found")

        await self._create_purchase_history(
            user_id=user_id,
            subscription=subscription,
            product_code=receipt_info.product_code,
            transaction_id=receipt_info.transaction_id,
            original_transaction_id=receipt_info.original_transaction_id,
            expires_date_ms=receipt_info.expires_date_ms,
            purchase_date_ms=receipt_info.purchase_date_ms,
            quantity=receipt_info.quantity,
            receipt_data=receipt_data,
        )

        item_inventory_products = await self._validate_purchase(product_code=receipt_info.product_code)

        await self._process_purchase(user_id=user_id, item_inventory_products=item_inventory_products)

    @staticmethod
    def _extract_latest_receipt_info(response: dict[str, Any]) -> dict[str, Any] | None:
        latest_receipt_info = response.get("latest_receipt_info")

        if isinstance(latest_receipt_info, list) and latest_receipt_info:
            return latest_receipt_info[0] or {}
        return None

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
        user_id: str,
        product_code: str,
        transaction_id: str,
        expires_date_ms: int,
    ) -> None:
        await Subscription.create_or_update_subscription(
            user_id=user_id,
            product_code=product_code,
            transaction_id=transaction_id,
            expires_date_ms=expires_date_ms,
            status=SubscriptionStatus.ACTIVE.value,
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
        receipt_data: str,
    ) -> None:
        await PurchaseHistory.create_purchase_history(
            user_id=user_id,
            subscription_id=subscription.subscription_id if subscription else None,
            product_code=product_code,
            transaction_id=transaction_id,
            original_transaction_id=original_transaction_id,
            status=PurchaseStatus.AVAILABLE.value,
            expires_date_ms=expires_date_ms,
            purchase_date_ms=purchase_date_ms,
            quantity=quantity,
            is_refunded=False,
            refunded_at=None,
            receipt_data=receipt_data,
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

    async def renew_subscription(self) -> dict[str, Any]:
        today = datetime.now(timezone(timedelta(hours=9)))

        subscriptions_to_renew = await Subscription.filter(
            expires_date__lte=today + timedelta(days=1), status="ACTIVE"
        ).select_related("user")

        for subscription in subscriptions_to_renew:

            purchase_history = await PurchaseHistory.filter(transaction_id=subscription.current_transaction_id).first()

            if purchase_history:
                response = await self._validate_apple_receipt(receipt_data=purchase_history.receipt_data)

                latest_receipt_info = self._extract_latest_receipt_info(response)

                if latest_receipt_info is None:
                    raise ValueError("No valid receipt information found.")

                receipt_data = await self._parse_receipt_info(latest_receipt_info)

                if not await self._check_auto_renewal(response.get("pending_renewal_info", [])):
                    continue

                await self._update_subscription_expiration(
                    subscription=subscription, expires_date_ms=receipt_data.expires_date_ms
                )

                await self._create_purchase_history(
                    user_id=str(uuid.UUID(bytes=subscription.user.user_id)),  # type: ignore
                    subscription=subscription,
                    product_code=receipt_data.product_code,
                    transaction_id=receipt_data.transaction_id,
                    original_transaction_id=receipt_data.original_transaction_id,
                    expires_date_ms=receipt_data.expires_date_ms,
                    purchase_date_ms=receipt_data.purchase_date_ms,
                    quantity=receipt_data.quantity,
                    receipt_data=purchase_history.receipt_data,
                )

        return {"message": "Subscription renewal completed successfully"}

    @staticmethod
    async def _update_subscription_expiration(subscription: Subscription, expires_date_ms: int) -> None:
        new_expires_date = datetime.fromtimestamp(expires_date_ms / 1000)
        subscription.expires_date = new_expires_date
        await subscription.save()

    @staticmethod
    async def _parse_receipt_info(latest_receipt_info: dict[str, Any]) -> ReceiptInfoDTO:
        return ReceiptInfoDTO.build(latest_receipt_info)

    @staticmethod
    async def _check_auto_renewal(pending_renewal_info: list[dict[str, Any]]) -> bool:
        if pending_renewal_info:
            auto_renew_status = pending_renewal_info[0].get("auto_renew_status")
            expiration_intent = pending_renewal_info[0].get("expiration_intent")

            if auto_renew_status == "0" or expiration_intent == "1":
                return False
        return True

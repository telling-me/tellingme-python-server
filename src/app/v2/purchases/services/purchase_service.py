import base64
import re

import httpx
from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from app.v2.cheese_managers.services.cheese_service import CheeseService
from app.v2.items.models.item import ItemInventory, ItemInventoryProductInventory, ProductInventory
from app.v2.purchases.models.purchase_history import PurchaseHistory
from app.v2.users.services.user_service import UserService
from core.configs import settings


class PurchaseService:
    @staticmethod
    async def process_krw_payment(product: ProductInventory, quantity: int) -> None:
        print(f"Processing KRW payment: {product.price * quantity} KRW")
        # 여기에 실제 KRW 결제 처리 로직 구현

    async def validate_receipt(self, receipt_data: str, user_id: str) -> dict:

        url = settings.APPLE_URL

        payload = {
            "receipt-data": receipt_data,
            "password": settings.APPLE_SHARED_SECRET,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            print(response.json())
        if response.status_code == 200:
            return await self._handle_receipt_response(response.json(), user_id)
        else:
            raise HTTPException(status_code=500, detail="Failed to connect to Apple server")

    async def receipt_test(self) -> dict:
        file_path = "/Users/gimtaeu/workspace/tellingme-python-server/1개월 구독한 영수증 data.txt/TXT.rtf"
        base64_data = self.extract_base64_from_rtf(file_path)

        url = settings.APPLE_URL

        payload = {
            "receipt-data": base64_data,
            "password": settings.APPLE_SHARED_SECRET,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response_data = response.json()
            print(response_data)
            if response.status_code != 200 or response_data.get("status") != 0:
                raise HTTPException(status_code=400, detail="Receipt verification failed")

            return response_data

    async def _handle_receipt_response(self, response_data: dict, user_id: str) -> dict:
        if response_data.get("status") == 0:
            in_app_purchase = response_data.get("receipt", {}).get("in_app", [])
            if in_app_purchase:
                purchase_info = in_app_purchase[0]
                return await self._save_purchase_history(user_id, purchase_info)
            else:
                raise HTTPException(status_code=400, detail="No in-app purchase found")
        else:
            raise HTTPException(status_code=400, detail="Invalid receipt")

    @classmethod
    async def _save_purchase_history(cls, user_id: str, purchase_info: dict) -> dict:
        receipt_id = purchase_info.get("transaction_id")
        product_code = purchase_info.get("product_id")
        status = "completed"

        existing_purchase = await PurchaseHistory.filter(receipt_id=receipt_id).exists()
        if existing_purchase:
            raise HTTPException(status_code=400, detail="Duplicate receipt")

        purchase_history = await PurchaseHistory.create(
            product_code=product_code,
            status=status,
            receipt_id=receipt_id,
            user_id=user_id,
        )
        return {
            "message": "Purchase history saved",
            "purchase_history_id": purchase_history.purchase_history_id,
        }

    @staticmethod
    async def validate_purchase(
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
    async def process_purchase(
        cls,
        item_inventory_products: list[ItemInventoryProductInventory],
        user_id: str,
        cheese_manager_id: str,
    ) -> None:
        for item_inventory_product in item_inventory_products:
            item: ItemInventory = await item_inventory_product.item_inventory
            quantity = item_inventory_product.quantity

            if item.item_category == "SUBSCRIPTION":
                await UserService.set_is_premium(user_id=user_id, is_premium=True)
            elif item.item_category == "CHEESE":
                await CheeseService.add_cheese(cheese_manager_id=cheese_manager_id, amount=quantity)
            else:
                raise ValueError(f"Invalid item category for purchase: {item.item_category}")

    # purchase_info = {
    #     "transaction_id": "1000000654000000",  # 고유한 거래 ID (영수증 ID로 사용 가능)
    #     "product_id": "com.example.app.product1",  # 구매한 상품의 ID
    #     "purchase_date": "2024-11-01T10:30:00Z",  # 구매한 날짜와 시간
    #     "original_transaction_id": "1000000654000000",  # 원래 거래 ID (구독 갱신 시 동일)
    #     "quantity": "1",  # 구매 수량
    #     "expires_date": "2024-12-01T10:30:00Z",  # 구독 만료 날짜 (구독형 상품인 경우)
    #     "is_trial_period": "false",  # 무료 체험 기간 여부
    #     "is_in_intro_offer_period": "false"  # 소개 할인 기간 여부
    # }

    # 소모성
    # purchase_info = {
    #     "transaction_id": "1000000654000000",
    #     "product_id": "com.example.app.product1",
    #     "purchase_date": "2024-11-01T10:30:00Z",
    # }

    # 구독
    # purchase_info = {
    #     "transaction_id": "1000000654000000",
    #     "product_id": "com.example.app.product1",
    #     "purchase_date": "2024-11-01T10:30:00Z",
    #     "expires_date": "2024-12-01T10:30:00Z",
    #     "original_transaction_id": "1000000654000000"
    # }

    import re
    import base64

    @staticmethod
    def extract_base64_from_rtf(file_path):
        # 파일 읽기
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
        except FileNotFoundError:
            raise ValueError(f"File not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Failed to read the file: {str(e)}")

        # Base64 데이터 추출 (MII로 시작하는 패턴만)
        base64_pattern = r"MII[A-Za-z0-9+/=]+"
        matches = re.findall(base64_pattern, content)

        if not matches:
            raise ValueError("No valid Base64 data found in the file.")

        # 가장 긴 Base64 데이터 선택
        base64_data = max(matches, key=len)

        # Base64 데이터 유효성 검증
        try:
            base64.b64decode(base64_data, validate=True)
        except Exception:
            raise ValueError("Extracted data is not valid Base64.")

        # 디버깅 로그 출력
        print(f"Extracted Base64 data length: {len(base64_data)}")

        return base64_data

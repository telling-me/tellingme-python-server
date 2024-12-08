from typing import Any, Optional

from pydantic import BaseModel

from app.v2.purchases.models.purchase_status import purchase_mapping
from common.base_models.base_dtos.base_response import BaseResponseDTO


class ReceiptInfoDTO(BaseModel):
    transaction_id: str
    original_transaction_id: str
    expires_date_ms: int
    purchase_date_ms: int
    product_code: str
    quantity: int
    cancellation_date_ms: Optional[int] = None

    @classmethod
    def build(cls, latest_receipt_info: dict[str, Any]) -> "ReceiptInfoDTO":
        transaction_id = latest_receipt_info["transaction_id"]
        original_transaction_id = latest_receipt_info["original_transaction_id"]
        expires_date_ms = int(latest_receipt_info.get("expires_date_ms", 0))
        purchase_date_ms = int(latest_receipt_info.get("purchase_date_ms", 0))
        product_code = purchase_mapping.get(latest_receipt_info["product_id"], latest_receipt_info["product_id"])
        quantity = int(latest_receipt_info.get("quantity", 1))
        cancellation_date_ms = latest_receipt_info.get("cancellation_date_ms")  # 환불일 (밀리초)

        return cls(
            transaction_id=transaction_id,
            original_transaction_id=original_transaction_id,
            expires_date_ms=expires_date_ms,
            purchase_date_ms=purchase_date_ms,
            product_code=product_code,
            quantity=quantity,
            cancellation_date_ms=cancellation_date_ms,
        )


class PurchaseDTO(BaseModel):
    productCode: str
    isPremium: bool

    @classmethod
    def build(cls, product_code: str, is_premium: bool) -> "PurchaseDTO":
        return cls(
            productCode=product_code,
            isPremium=is_premium,
        )


class PurchaseResponseDTO(BaseModel):
    message: str
    data: PurchaseDTO
    code: int

    @classmethod
    def build(cls, is_premium: bool, product_code: str) -> "PurchaseResponseDTO":
        return cls(
            code=200,
            message="Purchase successful.",
            data=PurchaseDTO.build(product_code=product_code, is_premium=is_premium),
        )

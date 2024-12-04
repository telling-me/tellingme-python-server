from typing import Any

from fastapi import APIRouter, Depends, status

from app.v2.purchases.dtos.requests import ReceiptRequestDTO
from app.v2.purchases.services.purchase_service import PurchaseService

router = APIRouter(prefix="/purchase", tags=["Purchase"])


@router.post(
    "/apple",
    status_code=status.HTTP_200_OK,
    response_model=dict[str, Any],
    summary="apple 결제 api",
    description="apple 결제 api",
)
async def process_receipt(
    receipt: ReceiptRequestDTO,
    purchase_service: PurchaseService = Depends(),
) -> dict[str, Any]:
    await purchase_service.process_apple_purchase(receipt_data=receipt.receiptData, user_id=receipt.user_id)
    return {
        "code": status.HTTP_200_OK,
        "message": "Receipt verified successfully",
        "data": True,
    }


@router.post("/receipt-test")
async def receipt_test(
    receipt: ReceiptRequestDTO,
    purchase_service: PurchaseService = Depends(),
) -> dict[str, Any]:
    return await purchase_service._validate_apple_receipt(receipt_data=receipt.receiptData)


@router.get("/renew-test")
async def renew_test(
    purchase_service: PurchaseService = Depends(),
) -> dict[str, Any]:
    return await purchase_service.renew_subscription()

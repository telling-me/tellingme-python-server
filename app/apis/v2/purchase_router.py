from typing import Any

from fastapi import APIRouter, Depends, status

from app.dtos.purchase.purchase_dto import PurchaseResponseDTO
from app.dtos.purchase.requests import ReceiptRequestDTO
from app.services.purchase_service import PurchaseService

purchase_router = APIRouter(prefix="/purchase", tags=["Purchase"])


@purchase_router.post(
    "/apple",
    status_code=status.HTTP_200_OK,
    response_model=PurchaseResponseDTO,
    summary="apple 결제 api",
    description="apple 결제 api",
)
async def process_receipt(
    receipt: ReceiptRequestDTO,
    purchase_service: PurchaseService = Depends(),
) -> PurchaseResponseDTO:
    return await purchase_service.process_apple_purchase(receipt_data=receipt.receiptData, user_id=receipt.user_id)


@purchase_router.post("/receipt-test")
async def receipt_test(
    receipt: ReceiptRequestDTO,
    purchase_service: PurchaseService = Depends(),
) -> dict[str, Any]:
    data = await purchase_service._validate_apple_receipt(receipt_data=receipt.receiptData)
    return {
        "code": 200,
        "data": data,
        "message": "정상처리되었습니다",
    }


@purchase_router.get("/renew-test")
async def renew_test(
    purchase_service: PurchaseService = Depends(),
) -> None:
    return await purchase_service.process_subscriptions_renewal()


@purchase_router.get("/expired-test")
async def expired_test(
    purchase_service: PurchaseService = Depends(),
) -> None:
    await purchase_service.expire_subscriptions()

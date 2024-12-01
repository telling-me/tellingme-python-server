from typing import Any

from fastapi import APIRouter, HTTPException, status
from tortoise.exceptions import DoesNotExist

from app.v2.purchases.dtos.requests import PurchaseRequest, ReceiptRequestDTO
from app.v2.purchases.services.purchase_service import PurchaseService
from app.v2.users.services.user_service import UserService

router = APIRouter(prefix="/purchase", tags=["Purchase"])


@router.post("/process-receipt")
async def process_receipt(receipt: ReceiptRequestDTO) -> dict[str, Any]:
    if not receipt.receiptData or not receipt.user_id:
        raise HTTPException(status_code=400, detail="Missing data")
    purchase_service = PurchaseService()
    data = await purchase_service.validate_receipt(receipt.receiptData, receipt.user_id)
    return {
        "code": status.HTTP_200_OK,
        "message": "Receipt verified successfully",
        "data": data,
    }


# @router.get("/receipt-test")
# async def receipt_test() -> dict[str, Any]:
#     purchase_service = PurchaseService()
#     return await purchase_service.receipt_test()


@router.post("")
async def process_purchase(request: PurchaseRequest) -> dict[str, str]:
    try:
        user_id = request.user_id
        product_code = request.product_code

        item_inventory_products = await PurchaseService.validate_purchase(product_code)

        user = await UserService.get_user_info(user_id=user_id)

        await PurchaseService.process_purchase(
            item_inventory_products=item_inventory_products,
            user_id=user_id,
            cheese_manager_id=user["cheese_manager_id"],
        )

        return {"message": "Purchase successful", "product": product_code}

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

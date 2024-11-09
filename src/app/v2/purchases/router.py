from fastapi import HTTPException, APIRouter
from tortoise.exceptions import DoesNotExist

from app.v2.items.models.item import (
    ProductInventory,
    ItemInventoryProductInventory,
    ItemInventory,
)
from app.v2.purchases.dtos.requests import ReceiptRequest
from app.v2.purchases.services.purchase_service import PurchaseService
from app.v2.users.services.user_service import UserService

router = APIRouter(prefix="/purchase", tags=["Purchase"])


@router.post("/process-receipt/")
async def process_receipt(receipt: ReceiptRequest):
    if not receipt.receipt_data or not receipt.user_id:
        raise HTTPException(status_code=400, detail="Missing data")
    purchase_service = PurchaseService()
    # Apple 서버에서 영수증 검증으로 이동
    return await purchase_service.validate_receipt(
        receipt.receipt_data, receipt.user_id
    )


@router.post("")
async def process_purchase(product_code: str):
    try:
        user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"

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

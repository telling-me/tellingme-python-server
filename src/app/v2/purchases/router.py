from fastapi import HTTPException, APIRouter
from tortoise.exceptions import DoesNotExist

from app.v2.items.models.item import (
    ProductInventory,
    ItemInventoryProductInventory,
    ItemInventory,
)
from app.v2.purchases.services.purchase_service import PurchaseService

router = APIRouter(prefix="/purchase", tags=["Purchase"])


@router.post("")
async def process_purchase(product_code: str):
    try:
        user_id = user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"

        product = await ProductInventory.get(product_code=product_code)

        if product.transaction_currency not in ["KRW", "CHEESE"]:
            raise HTTPException(
                status_code=400, detail="Invalid transaction currency for purchase."
            )

        item_inventory_products = await ItemInventoryProductInventory.filter(
            product_inventory_id=product.product_id
        ).all()

        if not item_inventory_products:
            raise HTTPException(
                status_code=404, detail="No inventory found for this product."
            )

        for item_inventory_product in item_inventory_products:
            item: ItemInventory = await item_inventory_product.item_inventory
            quantity = item_inventory_product.quantity

            if product.transaction_currency == "KRW":
                await PurchaseService.process_krw_payment(product, quantity)

            if item.item_category == "SUBSCRIPTION":
                await PurchaseService.process_subscription(
                    item, quantity, item_inventory_product.item_measurement
                )
            elif item.item_category == "POINT":
                await PurchaseService.add_points(user_id, quantity)
            elif item.item_category == "CHEESE":
                await PurchaseService.add_cheese(user_id, quantity)
            else:
                raise ValueError(
                    f"Invalid item category for purchase: {item.item_category}"
                )

        return {"message": "Purchase successful", "product": product}

    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

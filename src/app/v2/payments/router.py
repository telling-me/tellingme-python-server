from fastapi import APIRouter, HTTPException


from app.v2.payments.services.payment_service import PaymentService
from app.v2.users.services.user_service import UserService

router = APIRouter(prefix="/payment", tags=["Payment"])


# current_user: User = Depends(get_current_user)
@router.post("")
async def process_payment(product_code: str):
    try:
        user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"

        product, item_inventory_products = await PaymentService.validate_payment(
            product_code
        )

        user = await UserService.get_user_info(user_id=user_id)

        await PaymentService.process_cheese_payment(
            product, item_inventory_products, user_id, user["cheese_manager_id"]
        )

        return {"message": "Payment successful", "product": product}

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

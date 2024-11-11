from fastapi import APIRouter, HTTPException, status

from app.v2.payments.dtos.request import PaymentRequestDTO
from app.v2.payments.dtos.response import PaymentResponseDTO
from app.v2.payments.services.payment_service import PaymentService
from app.v2.users.services.user_service import UserService

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post(
    "",
    response_model=PaymentResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def process_payment(request: PaymentRequestDTO) -> PaymentResponseDTO:
    try:
        user_id = request.user_id
        product_code = request.productCode

        product, item_inventory_products = await PaymentService.validate_payment(
            product_code
        )

        user = await UserService.get_user_info(user_id=user_id)

        await PaymentService.process_cheese_payment(
            product, item_inventory_products, user_id, user["cheese_manager_id"]
        )
        return PaymentResponseDTO.builder(product_code=product.product_code)

    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

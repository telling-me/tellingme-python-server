from fastapi import APIRouter, status

from app.dtos.payment.payment_request import PaymentRequest
from app.dtos.payment.payment_response import PaymentResponse, ProductDTO
from app.services.payment_service import PaymentService

payment_router = APIRouter(prefix="/payment", tags=["Payment"])


@payment_router.post(
    "",
    response_model=PaymentResponse,
    status_code=status.HTTP_200_OK,
)
async def process_payment(payment_request: PaymentRequest) -> PaymentResponse:
    return PaymentResponse(
        code=status.HTTP_200_OK,
        data=ProductDTO(
            product_code=await PaymentService.process_cheese_payment(
                product_code=payment_request.productCode, user_id=payment_request.user_id
            ),
        ),
        message="Payment successful",
    )

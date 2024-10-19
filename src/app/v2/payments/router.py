from fastapi import APIRouter

from app.v2.payments.dtos.request import PaymentRequestDTO

router = APIRouter(prefix="/payment", tags=["Payment"])


@router.post(
    "",
)
async def payment_item_handler(
    body: PaymentRequestDTO,
):
    prodict_id = body.productId

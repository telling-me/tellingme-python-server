from pydantic import BaseModel


class PaymentRequestDTO(BaseModel):
    productId: str

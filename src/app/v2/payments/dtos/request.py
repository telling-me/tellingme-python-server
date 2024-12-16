from pydantic import BaseModel


class PaymentRequestDTO(BaseModel):
    user_id: str
    productCode: str

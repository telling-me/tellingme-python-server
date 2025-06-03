from pydantic import BaseModel


class PaymentRequest(BaseModel):
    user_id: str
    productCode: str

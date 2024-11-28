from pydantic import BaseModel


class ReceiptRequestDTO(BaseModel):
    receiptData: str
    user_id: str


class PurchaseRequest(BaseModel):
    user_id: str
    product_code: str

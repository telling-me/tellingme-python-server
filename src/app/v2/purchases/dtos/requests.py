from pydantic import BaseModel


class ReceiptRequest(BaseModel):
    receipt_data: str
    user_id: str


class PurchaseRequest(BaseModel):
    user_id: str
    product_code: str

from pydantic import BaseModel


class ReceiptRequest(BaseModel):
    receipt_data: str
    user_id: str

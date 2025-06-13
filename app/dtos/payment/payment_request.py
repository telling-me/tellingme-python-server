from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class PaymentRequest(BaseModel):
    model_config = FROZEN_CONFIG

    user_id: str
    productCode: str

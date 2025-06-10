from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO
from app.dtos.frozen_config import FROZEN_CONFIG


class ProductDTO(BaseModel):
    model_config = FROZEN_CONFIG

    product_code: str


class PaymentResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: ProductDTO

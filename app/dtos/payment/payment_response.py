from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO


class ProductDTO(BaseModel):
    product_code: str


class PaymentResponse(BaseResponseDTO):
    data: ProductDTO

from pydantic import BaseModel
from common.base_models.base_dtos.base_response import BaseResponseDTO


class ProductDTO(BaseModel):
    product_code: str


class PaymentResponseDTO(BaseResponseDTO):
    data: ProductDTO

    @classmethod
    def builder(cls, product_code: str) -> "PaymentResponseDTO":
        return cls(
            code=200,
            message="Payment successful",
            data=ProductDTO(
                product_code=product_code,
            ),
        )

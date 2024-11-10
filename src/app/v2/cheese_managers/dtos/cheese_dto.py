from pydantic import BaseModel
from common.base_models.base_dtos.base_response import BaseResponseDTO


class CheeseDTO(BaseModel):
    cheeseBalance: int

    @classmethod
    def builder(cls, cheese_balance: int) -> "CheeseDTO":
        return cls(cheeseBalance=cheese_balance)


class CheeseResponseDTO(BaseResponseDTO):
    data: CheeseDTO

    @classmethod
    def builder(cls, cheese_balance: int) -> "CheeseResponseDTO":
        return cls(
            code=200,
            message="success",
            data=CheeseDTO.builder(cheese_balance=cheese_balance),
        )

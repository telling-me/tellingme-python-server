from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO


class TotalCheeseAmount(BaseModel):
    cheeseBalance: int


class CheeseResponse(BaseResponseDTO):
    data: TotalCheeseAmount

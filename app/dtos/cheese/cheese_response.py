from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO
from app.dtos.frozen_config import FROZEN_CONFIG


class TotalCheeseAmount(BaseModel):
    model_config = FROZEN_CONFIG

    cheeseBalance: int


class CheeseResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: TotalCheeseAmount

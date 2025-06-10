from app.dtos.base_response import BaseResponseDTO
from app.dtos.color.color_dto import ColorDTO
from app.dtos.frozen_config import FROZEN_CONFIG


class ColorsResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: list[ColorDTO]

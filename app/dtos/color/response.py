from app.dtos.color.color_dto import ColorDTO
from app.common.base_models.base_dtos.base_response import BaseResponseDTO


class ColorListResponseDTO(BaseResponseDTO):
    data: list[ColorDTO]

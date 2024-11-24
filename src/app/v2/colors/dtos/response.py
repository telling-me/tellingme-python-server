from app.v2.colors.dtos.color_dto import ColorDTO
from common.base_models.base_dtos.base_response import BaseResponseDTO


class ColorListResponseDTO(BaseResponseDTO):
    data: list[ColorDTO]

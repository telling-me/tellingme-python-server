from app.dtos.base_response import BaseResponseDTO
from app.dtos.color.color_dto import ColorDTO


class ColorListResponseDTO(BaseResponseDTO):
    data: list[ColorDTO]

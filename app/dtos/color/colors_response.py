from app.dtos.base_response import BaseResponseDTO
from app.dtos.color.color_dto import ColorDTO


class ColorsResponse(BaseResponseDTO):
    data: list[ColorDTO]

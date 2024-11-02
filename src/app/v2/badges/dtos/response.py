from app.v2.badges.dtos.badge_dto import BadgeDTO
from common.base_models.base_dtos.base_response import BaseResponseDTO


class BadgeListResponseDTO(BaseResponseDTO):
    data: list[BadgeDTO]

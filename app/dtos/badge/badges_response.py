from app.dtos.base_response import BaseResponseDTO
from app.dtos.badge.badge_dto import BadgeDTO
from app.dtos.frozen_config import FROZEN_CONFIG


class BadgesResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: list[BadgeDTO]

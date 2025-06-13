from pydantic import BaseModel

from app.dtos.badge.badge_dto import BadgeDTO
from app.dtos.color.color_dto import ColorDTO
from app.dtos.frozen_config import FROZEN_CONFIG
from app.dtos.level.level_info_dto import LevelInfoDTO
from app.dtos.user.user_info_dto import UserInfoDTO


class DataDTO(BaseModel):
    model_config = FROZEN_CONFIG

    badges: list[BadgeDTO]
    colors: list[ColorDTO]
    userInfo: UserInfoDTO
    levelInfo: LevelInfoDTO
    recordCount: int = 0

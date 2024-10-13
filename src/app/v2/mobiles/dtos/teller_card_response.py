from pydantic import BaseModel
from typing import List, Optional

from app.v2.badges.dtos.badge_dto import BadgeCodeDTO
from app.v2.colors.dtos.color_dto import ColorCodeDTO
from app.v2.levels.dtos.level_dto import LevelDTO

from app.v2.users.dtos.user_info_dto import UserInfoDTO


class DataDTO(BaseModel):
    badges: List[BadgeCodeDTO]
    colors: List[ColorCodeDTO]
    userInfo: UserInfoDTO
    level: LevelDTO


# 최종 응답 DTO
class TellerCardResponseDTO(BaseModel):
    data: DataDTO

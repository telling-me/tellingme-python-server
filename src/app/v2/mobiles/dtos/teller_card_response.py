from pydantic import BaseModel
from typing import List, Optional

from app.v2.badges.dtos.badge_dto import BadgeDTO
from app.v2.colors.dtos.color_dto import ColorCodeDTO
from app.v2.levels.dtos.level_dto import LevelDTO

from app.v2.users.dtos.user_info_dto import UserInfoDTO
from common.base_models.base_dtos.base_response import BaseResponseDTO


class DataDTO(BaseModel):
    badges: List[BadgeDTO]
    colors: List[ColorCodeDTO]
    userInfo: UserInfoDTO
    level: LevelDTO

    @classmethod
    def builder(
        cls,
        badges: List[BadgeDTO],
        colors: List[ColorCodeDTO],
        userInfo: UserInfoDTO,
        level: LevelDTO,
    ) -> "DataDTO":
        return cls(
            badges=badges,
            colors=colors,
            userInfo=userInfo,
            level=level,
        )


# 최종 응답 DTO
class TellerCardResponseDTO(BaseResponseDTO):
    data: DataDTO

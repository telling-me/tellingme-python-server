from typing import Optional

from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO
from app.dtos.badge.badge_dto import BadgeDTO
from app.dtos.color.color_dto import ColorDTO
from app.dtos.level.level_dto import LevelInfoDTO
from app.dtos.user.user_info_dto import UserInfoDTO


class DataDTO(BaseModel):
    badges: list[BadgeDTO]
    colors: list[ColorDTO]
    userInfo: UserInfoDTO
    levelInfo: LevelInfoDTO
    recordCount: int = 0

    @classmethod
    def builder(
        cls,
        badges: list[BadgeDTO],
        colors: list[ColorDTO],
        userInfo: UserInfoDTO,
        levelInfo: LevelInfoDTO,
        recordCount: Optional[int] = None,
    ) -> "DataDTO":
        return cls(
            badges=badges,
            colors=colors,
            userInfo=userInfo,
            levelInfo=levelInfo,
            recordCount=recordCount if recordCount is not None else 0,
        )


# 최종 응답 DTO
class TellerCardResponseDTO(BaseResponseDTO):
    data: DataDTO

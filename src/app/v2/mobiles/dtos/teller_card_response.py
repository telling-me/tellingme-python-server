from typing import List, Optional

from pydantic import BaseModel

from app.v2.badges.dtos.badge_dto import BadgeDTO
from app.v2.colors.dtos.color_dto import ColorCodeDTO
from app.v2.levels.dtos.level_dto import LevelDTO, LevelInfoDTO
from app.v2.users.dtos.user_info_dto import UserInfoDTO
from common.base_models.base_dtos.base_response import BaseResponseDTO


class DataDTO(BaseModel):
    badges: List[BadgeDTO]
    colors: List[ColorCodeDTO]
    userInfo: UserInfoDTO
    levelInfo: LevelInfoDTO
    recordCount: int = 0

    @classmethod
    def builder(
        cls,
        badges: List[BadgeDTO],
        colors: List[ColorCodeDTO],
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

from typing import Optional

from pydantic import BaseModel

from app.apis.v2.badges.dtos.badge_dto import BadgeDTO
from app.apis.v2.colors.dtos.color_dto import ColorDTO
from app.apis.v2.levels.dtos.level_dto import LevelInfoDTO
from app.apis.v2.users.dtos.user_info_dto import UserInfoDTO
from app.common.base_models.base_dtos.base_response import BaseResponseDTO


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

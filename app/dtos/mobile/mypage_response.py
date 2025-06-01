from pydantic import BaseModel

from app.dtos.level.level_dto import LevelInfoDTO
from app.dtos.user.user_profile_dto import UserProfileDTO
from app.common.base_models.base_dtos.base_response import BaseResponseDTO


class UserProfileWithLevel(BaseModel):
    userProfile: UserProfileDTO
    level: LevelInfoDTO

    @classmethod
    def builder(
        cls,
        userProfile: UserProfileDTO,
        level: LevelInfoDTO,
    ) -> "UserProfileWithLevel":
        return cls(
            userProfile=userProfile,
            level=level,
        )


class MyPageResponseDTO(BaseResponseDTO):
    data: UserProfileWithLevel

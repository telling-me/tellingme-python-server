from pydantic import BaseModel

from app.apis.v2.levels.dtos.level_dto import LevelInfoDTO
from app.apis.v2.users.dtos.user_profile_dto import UserProfileDTO
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

from pydantic import BaseModel

from app.v2.levels.dtos.level_dto import LevelDto
from app.v2.users.dtos.user_profile_dto import UserProfileDto
from common.base_models.base_dtos.base_response import BaseResponseDTO


class UserProfileWithLevel(BaseModel):
    userProfile: UserProfileDto
    level: LevelDto


class UserProfileWithLevelResponseDTO(BaseResponseDTO):
    data: UserProfileWithLevel

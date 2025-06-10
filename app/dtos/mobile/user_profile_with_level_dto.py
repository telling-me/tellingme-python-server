from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG
from app.dtos.level.level_info_dto import LevelInfoDTO
from app.dtos.user.user_profile_dto import UserProfileDTO


class UserProfileWithLevelDTO(BaseModel):
    model_config = FROZEN_CONFIG

    userProfile: UserProfileDTO
    level: LevelInfoDTO

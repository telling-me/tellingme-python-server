from app.dtos.base_response import BaseResponseDTO
from app.dtos.frozen_config import FROZEN_CONFIG
from app.dtos.mobile.user_profile_with_level_dto import UserProfileWithLevelDTO


class MyPageResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: UserProfileWithLevelDTO

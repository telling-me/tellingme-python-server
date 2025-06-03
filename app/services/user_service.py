from typing import Any

from app.dtos.user.user_data import UserData
from app.dtos.user.user_dto import UserDTO, UserProfileData
from app.models.user import User


class UserService:
    @staticmethod
    async def get_user_info(user_id: str) -> UserData:
        result = await User.get_user_info_by_user_id(user_id=user_id)
        return UserData(**result)

    @classmethod
    async def get_user_profile(cls, user_id: str) -> UserProfileData:
        return await User.get_user_profile_by_user_id(user_id=user_id)

    @staticmethod
    async def set_is_premium(user_id: str, is_premium: bool) -> None:
        await User.set_is_premium(user_id=user_id, is_premium=is_premium)

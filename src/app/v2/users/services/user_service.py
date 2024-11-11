from app.v2.cheese_managers.models.cheese_manager import CheeseManager
from app.v2.users.models.user import User


class UserService:
    @staticmethod
    async def get_user_info(user_id: str) -> dict:
        return await User.get_user_info_by_user_id(user_id=user_id)

    @classmethod
    async def get_user_profile(cls, user_id: str) -> dict:
        return await User.get_user_profile_by_user_id(user_id=user_id)

    @staticmethod
    async def set_is_premium(user_id: str, is_premium: bool) -> None:
        await User.set_is_premium(user_id=user_id, is_premium=is_premium)

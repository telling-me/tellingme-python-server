from app.services.level_service import LevelService
from app.services.user_service import UserService


class UserMother:

    @staticmethod
    async def create_user(
        is_premium: bool = False,
    ) -> str:
        user_service = UserService()
        new_user_id = await user_service.create_user(is_premium=is_premium)
        return new_user_id

    @staticmethod
    async def create_level_inventory() -> None:
        level_service = LevelService()
        await level_service.create_level_inventory()

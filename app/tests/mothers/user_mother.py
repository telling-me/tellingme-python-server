from app.models.cheese_manager import CheeseManager
from app.services.level_service import LevelService
from app.services.user_service import UserService


class UserMother:

    @staticmethod
    async def create_user(
        user_name: str = "test_user",
        is_premium: bool = False,
    ) -> str:
        user_service = UserService()
        new_user_id = await user_service.create_user(user_name=user_name, is_premium=is_premium)
        return new_user_id

    @staticmethod
    async def add_cheese(user_id: str, amount: int) -> None:
        user = await UserService.get_user_info(user_id=user_id)
        await CheeseManager.add_cheese(cheese_manager_id=user.cheese_manager_id, amount=amount)

    @staticmethod
    async def create_level_inventory() -> None:
        level_service = LevelService()
        await level_service.create_level_inventory()

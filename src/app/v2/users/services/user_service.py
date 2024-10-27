from app.v2.cheese_managers.models.cheese_manager import CheeseManager
from app.v2.users.models.user import User


class UserService:
    @classmethod
    async def get_user_info(cls, user_id: str) -> dict:
        return await User.get_user_info_by_user_id(user_id=user_id)

    @classmethod
    async def get_cheese_balance(cls, cheese_manager_id: str) -> int:
        return await CheeseManager.get_total_cheese_amount_by_manager()

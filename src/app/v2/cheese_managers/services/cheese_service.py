from app.v2.cheese_managers.models.cheese_manager import CheeseManager


class CheeseService:

    @classmethod
    async def get_cheese_balance(cls, cheese_manager_id: int) -> int:
        return await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=cheese_manager_id) or 0

    @classmethod
    async def add_cheese(cls, cheese_manager_id: int, amount: int) -> None:
        await CheeseManager.add_cheese(cheese_manager_id=cheese_manager_id, amount=amount)

from app.v2.cheese_managers.models.cheese_manager import CheeseManager


class CheeseService:

    @classmethod
    async def get_cheese_balance(cls, cheese_manager_id: str) -> int:
        return await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=cheese_manager_id)

    @classmethod
    async def add_cheese(cls, cheese_manager_id: str, amount: int) -> None:
        await CheeseManager.add_cheese(cheese_manager_id=cheese_manager_id, amount=amount)

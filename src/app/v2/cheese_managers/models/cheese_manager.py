from tortoise import fields
from tortoise.expressions import Q
from tortoise.functions import Sum
from tortoise.models import Model
from tortoise.transactions import atomic

from app.v2.cheese_managers.models.cheese_status import CheeseStatus


class CheeseManager(Model):
    cheese_manager_id = fields.BigIntField(pk=True)  # BIGINT auto_increment equivalent

    class Meta:
        table = "cheese_manager"  # Database table name

    @staticmethod
    async def get_total_cheese_amount_by_manager(cheese_manager_id: int) -> int:
        result = (
            await CheeseHistory.filter(
                Q(status=CheeseStatus.CAN_USE) | Q(status=CheeseStatus.USING),
                cheese_manager_id=cheese_manager_id,
            )
            .annotate(total_cheese_amount=Sum("current_amount"))
            .values("total_cheese_amount")
        )

        return result[0].get("total_cheese_amount", 0)

    @staticmethod
    async def use_cheese(cheese_manager_id: int, amount: int) -> None:
        using_cheese = await CheeseHistory.filter(
            status=CheeseStatus.USING, cheese_manager_id=cheese_manager_id
        ).order_by("cheese_history_id")

        remaining_amount = amount

        for cheese in using_cheese:
            if cheese.current_amount >= remaining_amount:
                cheese.current_amount -= remaining_amount
                if cheese.current_amount == 0:
                    cheese.status = CheeseStatus.ALREADY_USED
                await cheese.save()
                return

            remaining_amount -= cheese.current_amount
            cheese.current_amount = 0
            cheese.status = CheeseStatus.ALREADY_USED
            await cheese.save()

        can_use_cheese = await CheeseHistory.filter(
            status=CheeseStatus.CAN_USE, cheese_manager_id=cheese_manager_id
        ).order_by("cheese_history_id")

        for cheese in can_use_cheese:
            if cheese.current_amount >= remaining_amount:
                cheese.current_amount -= remaining_amount
                cheese.status = CheeseStatus.USING
                await cheese.save()
                return

            remaining_amount -= cheese.current_amount
            cheese.current_amount = 0
            cheese.status = CheeseStatus.ALREADY_USED
            await cheese.save()

        if remaining_amount > 0:
            raise ValueError("Not enough cheese to complete the transaction")

    async def add_cheese(self, amount: int) -> None:
        await CheeseHistory.create(
            status=CheeseStatus.CAN_USE,
            current_amount=amount,
            starting_amount=amount,
            cheese_manager_id=self.cheese_manager_id,
        )


class CheeseHistory(Model):
    cheese_history_id = fields.BigIntField(pk=True)
    status = fields.CharEnumField(CheeseStatus, max_length=50, null=True)  # Enum Field
    current_amount = fields.IntField()
    starting_amount = fields.IntField()
    cheese_manager = fields.ForeignKeyField(
        "models.CheeseManager",
        related_name="histories",
        null=True,
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "cheese_history"

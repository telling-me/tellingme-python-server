from tortoise import fields
from tortoise.expressions import Q
from tortoise.functions import Sum
from tortoise.models import Model

from app.v2.cheese_managers.models.cheese_status import CheeseStatus


class CheeseManager(Model):
    cheese_manager_id = fields.BigIntField(pk=True)  # BIGINT auto_increment equivalent

    class Meta:
        table = "cheese_manager"  # Database table name

    async def get_total_cheese_amount_by_manager(cheese_manager_id: int):
        result = (
            await CheeseHistory.filter(
                Q(status=CheeseStatus.CAN_USE) | Q(status=CheeseStatus.USING),
                cheese_manager_id=cheese_manager_id,
            )
            .annotate(total_cheese_amount=Sum("current_amount"))
            .values("total_cheese_amount")
        )

        return result[0].get("total_cheese_amount", 0)


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

    class Meta:
        table = "cheese_history"  # Database table name

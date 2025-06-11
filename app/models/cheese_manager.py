from __future__ import annotations

from typing import cast

from tortoise import fields
from tortoise.expressions import Q
from tortoise.fields import ForeignKeyRelation
from tortoise.functions import Sum
from tortoise.models import Model

from app.common.constants.cheese_status import CheeseStatus


class CheeseManager(Model):
    """
    Cheese Manager 치즈 관련 작업을 하는 모델 겸 서비스
    """

    cheese_manager_id = fields.BigIntField(primary_key=True)

    class Meta:
        table = "cheese_manager"

    @staticmethod
    async def get_total_cheese_amount_by_manager(cheese_manager_id: int) -> int:
        return await CheeseHistory.get_total_amount_by_manager(cheese_manager_id)

    @classmethod
    async def use_cheese(cls, cheese_manager_id: int, amount: int) -> None:
        remaining = amount

        using_cheeses = await CheeseHistory.get_using_cheeses(cheese_manager_id)
        for cheese in using_cheeses:
            if cheese.current_amount >= remaining:
                cheese.current_amount -= remaining
                if cheese.current_amount == 0:
                    cheese.status = CheeseStatus.ALREADY_USED
                await cheese.save()
                return
            else:
                remaining -= cheese.current_amount
                cheese.current_amount = 0
                cheese.status = CheeseStatus.ALREADY_USED
                await cheese.save()

        can_use_cheeses = await CheeseHistory.get_can_use_cheeses(cheese_manager_id)

        for cheese in can_use_cheeses:
            if cheese.current_amount >= remaining:
                cheese.current_amount -= remaining
                cheese.status = CheeseStatus.USING if cheese.current_amount > 0 else CheeseStatus.ALREADY_USED
                await cheese.save()
                return
            else:
                remaining -= cheese.current_amount
                cheese.current_amount = 0
                cheese.status = CheeseStatus.ALREADY_USED
                await cheese.save()

    @staticmethod
    async def add_cheese(cheese_manager_id: int, amount: int) -> None:
        await CheeseHistory.create(
            status=CheeseStatus.CAN_USE,
            current_amount=amount,
            starting_amount=amount,
            cheese_manager_id=cheese_manager_id,
        )


class CheeseHistory(Model):
    cheese_history_id = fields.BigIntField(primary_key=True)
    status = fields.CharEnumField(CheeseStatus, max_length=50, null=True)
    current_amount = fields.IntField()
    starting_amount = fields.IntField()
    cheese_manager: ForeignKeyRelation[CheeseManager] = fields.ForeignKeyField(
        "models.CheeseManager",
        related_name="histories",
        on_delete=fields.CASCADE,
    )

    class Meta:
        table = "cheese_history"

    @classmethod
    async def get_total_amount_by_manager(cls, manager_id: int) -> int:
        result = cast(
            list[int | None],
            await (
                cls.filter(
                    Q(status=CheeseStatus.CAN_USE) | Q(status=CheeseStatus.USING),
                    cheese_manager_id=manager_id,
                )
                .annotate(total=Sum("current_amount"))
                .values_list("total", flat=True)
            ),
        )

        return result[0] if result and result[0] is not None else 0

    @classmethod
    async def get_using_cheeses(cls, manager_id: int) -> list[CheeseHistory]:
        return await cls.filter(status=CheeseStatus.USING, cheese_manager_id=manager_id).order_by("cheese_history_id")

    @classmethod
    async def get_can_use_cheeses(cls, manager_id: int) -> list[CheeseHistory]:
        return await cls.filter(status=CheeseStatus.CAN_USE, cheese_manager_id=manager_id).order_by("cheese_history_id")

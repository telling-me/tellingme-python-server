from tortoise import fields
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.dtos.level.level_data import LevelData
from app.queries.level_query import (
    SELECT_USER_LEVEL_AND_REQUIRED_EXP_QUERY,
    UPDATE_USER_LEVEL_AND_EXP_QUERY,
)


class Level(Model):
    level_id = fields.BigIntField(primary_key=True)
    user_exp = fields.IntField()
    user_level = fields.IntField()

    class Meta:
        table = "level"

    @classmethod
    async def get_level_info(cls, user_id: str) -> LevelData:
        query = SELECT_USER_LEVEL_AND_REQUIRED_EXP_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=(value,), fetch_type="single")
        return LevelData(**result)

    @classmethod
    async def update_level_and_exp(cls, user_id: str, new_level: int, new_exp: int) -> None:
        query = UPDATE_USER_LEVEL_AND_EXP_QUERY
        values = (new_level, new_exp, user_id)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")


class LevelInventory(Model):
    level_inventory_id = fields.BigIntField(primary_key=True)
    level = fields.IntField(null=True)
    required_exp = fields.IntField(null=True)

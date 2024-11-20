from tortoise import fields
from tortoise.models import Model

from app.v2.levels.querys.level_query import (
    SELECT_USER_EXP_QUERY,
    SELECT_USER_LEVEL_AND_EXP_BY_USER_UUID_QUERY,
    SELECT_USER_LEVEL_AND_REQUIRED_EXP_QUERY,
    UPDATE_USER_LEVEL_AND_EXP_QUERY,
)
from common.utils.query_executor import QueryExecutor


class Level(Model):
    level_id = fields.BigIntField(pk=True)
    user_exp = fields.IntField()
    user_level = fields.IntField()

    class Meta:
        table = "level"

    @classmethod
    async def get_level_info(cls, user_id: str) -> dict | None:
        query = SELECT_USER_LEVEL_AND_REQUIRED_EXP_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=(value,), fetch_type="single")

    @classmethod
    async def update_level_and_exp(cls, user_id: str, new_level: int, new_exp: int) -> None:
        query = UPDATE_USER_LEVEL_AND_EXP_QUERY
        values = (new_level, new_exp, user_id)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")


class LevelInventory(Model):
    level_inventory_id = fields.BigIntField(pk=True)
    level = fields.IntField(null=True)
    required_exp = fields.IntField(null=True)

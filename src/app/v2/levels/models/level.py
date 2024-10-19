from tortoise import fields
from tortoise.models import Model

from app.v2.levels.querys.level_query import (
    SELECT_USER_LEVEL_AND_EXP_BY_USER_UUID_QUERY,
)
from common.utils.query_executor import QueryExecutor


class Level(Model):
    level_id = fields.BigIntField(pk=True)  # BIGINT auto_increment equivalent
    user_exp = fields.IntField()  # Experience points field
    user_level = fields.IntField()  # User level field

    class Meta:
        table = "level"

    @classmethod
    async def get_level_info_by_user_id(cls, user_id: str) -> dict | None:
        query = SELECT_USER_LEVEL_AND_EXP_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(
            query, values=value, fetch_type="single"
        )

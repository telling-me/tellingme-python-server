from __future__ import annotations

from tortoise import fields
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.dtos.badge.badge_data import BadgeData
from app.queries.badge_query import (
    INSERT_BADGE_CODE_FOR_USER_QUERY,
    SELECT_BADGE_BY_USER_UUID_QUERY,
    SELECT_BADGE_COUNT_BY_USER_UUID_QUERY,
)


class Badge(Model):
    badge_id = fields.BigIntField(primary_key=True)
    badge_code = fields.CharField(max_length=255)
    user_id = fields.BinaryField(max_length=16, null=True)

    class Meta:
        table = "badge"

    @classmethod
    async def get_badge_count_by_user_id(cls, user_id: str) -> int:
        query = SELECT_BADGE_COUNT_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return int(result.get("badge_count", 0) if result else 0)

    @classmethod
    async def get_badges_with_details_by_user_id(cls, user_id: str) -> list[BadgeData]:
        query = SELECT_BADGE_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="multiple")
        return [BadgeData(**row) for row in result]

    @classmethod
    async def create_by_user_id(cls, user_id: str, badge_code: str) -> None:
        query = INSERT_BADGE_CODE_FOR_USER_QUERY
        values = (badge_code, user_id)
        await QueryExecutor.execute_query(query, values=values)

from tortoise import fields
from tortoise.models import Model

from app.v2.badges.querys.badge_query import (
    SELECT_BADGE_COUNT_AND_CODES_BY_USER_UUID_QUERY,
    SELECT_BADGE_BY_USER_UUID_QUERY,
    SELECT_BADGE_CODE_BY_USER_UUID_QUERY,
)

from common.utils.query_executor import QueryExecutor


class Badge(Model):
    badge_id = fields.BigIntField(pk=True)  # 자동 증가하는 기본 키
    badge_code = fields.CharField(max_length=255, null=True)  # 배지 코드
    user = fields.ForeignKeyField("models.User", related_name="badges", null=True)

    class Meta:
        table = "badge"

    @classmethod
    async def get_badge_count_and_codes_by_user_id(cls, user_id: str) -> tuple:

        query = SELECT_BADGE_COUNT_AND_CODES_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(
            query, values=value, fetch_type="multiple"
        )

        return (
            (result[0].get("badge_count", 0), result[0].get("badge_code", ""))
            if result and len(result) > 0
            else (0, "")
        )

    @classmethod
    async def get_badges_with_details_by_user_id(cls, user_id: str) -> list:
        query = SELECT_BADGE_BY_USER_UUID_QUERY
        value = user_id

        result = await QueryExecutor.execute_query(
            query, values=value, fetch_type="multiple"
        )

        return result if result else []

    @classmethod
    async def get_badge_codes_by_user_id(cls, user_id: str) -> list[dict]:
        query = SELECT_BADGE_CODE_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(
            query, values=value, fetch_type="multiple"
        )

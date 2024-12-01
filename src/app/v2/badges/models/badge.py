from typing import Any

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.badges.querys.badge_query import (
    INSERT_BADGE_CODE_FOR_USER_QUERY,
    SELECT_BADGE_BY_USER_UUID_QUERY,
    SELECT_BADGE_CODE_BY_USER_UUID_QUERY,
    SELECT_BADGE_COUNT_BY_USER_UUID_QUERY,
)
from app.v2.users.models.user import User
from common.utils.query_executor import QueryExecutor


class Badge(Model):
    badge_id = fields.BigIntField(pk=True)
    badge_code = fields.CharField(max_length=255)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="badges")

    class Meta:
        table = "badge"

    @classmethod
    async def get_badge_count_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_BADGE_COUNT_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="single")

    @classmethod
    async def get_badges_with_details_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_BADGE_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="multiple")

    @classmethod
    async def get_badge_codes_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_BADGE_CODE_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="multiple")

    @classmethod
    async def add_badge(cls, user_id: str, badge_code: str) -> None:
        query = INSERT_BADGE_CODE_FOR_USER_QUERY
        values = (badge_code, user_id)
        await QueryExecutor.execute_query(query, values=values)


class BadgeInventory(Model):
    badge_code = fields.CharField(max_length=255, primary_key=True)
    badge_name = fields.CharField(max_length=255, null=True)
    badge_condition = fields.CharField(max_length=255, null=True)
    badge_middle_name = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "badge_inventory"

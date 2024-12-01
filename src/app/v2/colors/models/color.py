from typing import Any

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.colors.querys.color_query import (
    INSERT_COLOR_CODE_FOR_USER_QUERY,
    SELECT_COLOR_BY_USER_UUID_QUERY,
    SELECT_COLOR_CODE_BY_USER_UUID_QUERY,
)
from app.v2.users.models.user import User
from common.utils.query_executor import QueryExecutor


class Color(Model):
    color_id = fields.BigIntField(pk=True)
    color_code = fields.CharField(max_length=255, null=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="colors", on_delete=fields.CASCADE
    )

    class Meta:
        table = "color"

    @classmethod
    async def get_color_codes_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_COLOR_CODE_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="multiple")

    @classmethod
    async def add_color_code_for_user(cls, user_id: str, color_code: str) -> Any:
        query = INSERT_COLOR_CODE_FOR_USER_QUERY
        values = (color_code, user_id)
        return await QueryExecutor.execute_query(query, values=values, fetch_type="single")

    @classmethod
    async def get_colors_with_details_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_COLOR_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="multiple")


class ColorInventory(Model):
    color_code = fields.CharField(max_length=255, primary_key=True)
    color_name = fields.CharField(max_length=255, null=True)
    color_hex_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "color_inventory"  # 테이블 이름을 명시

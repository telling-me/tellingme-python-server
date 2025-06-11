from typing import Any

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.dtos.color.color_data import ColorData
from app.models.user import User
from app.queries.color_query import (
    INSERT_COLOR_CODE_FOR_USER_QUERY,
    SELECT_COLOR_BY_USER_UUID_QUERY,
)


class Color(Model):
    color_id = fields.BigIntField(primary_key=True)
    color_code = fields.CharField(max_length=255, null=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="colors", on_delete=fields.CASCADE
    )

    class Meta:
        table = "color"

    @classmethod
    async def create_by_user_id(cls, user_id: str, color_code: str) -> None:
        query = INSERT_COLOR_CODE_FOR_USER_QUERY
        values = (color_code, user_id)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")

    @classmethod
    async def get_colors_with_details_by_user_id(cls, user_id: str) -> list[ColorData]:
        query = SELECT_COLOR_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="multiple")
        return [ColorData(**row) for row in result]

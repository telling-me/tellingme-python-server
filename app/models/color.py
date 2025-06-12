from datetime import datetime, timedelta, timezone

from tortoise import fields
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.dtos.color.color_data import ColorData
from app.queries.color_query import (
    INSERT_COLOR_CODE_FOR_USER_QUERY,
    SELECT_COLOR_BY_USER_UUID_QUERY,
)


class Color(Model):
    color_id = fields.BigIntField(primary_key=True)
    color_code = fields.CharField(max_length=255, null=True)
    user_id = fields.BinaryField(max_length=16, null=True)

    class Meta:
        table = "color"

    @classmethod
    async def create_default_by_user_id(cls, user_id: str) -> None:
        color_codes = ["CL_DEFAULT", "CL_BLUE_001", "CL_ORANGE_001"]
        now_kst = datetime.now(timezone(timedelta(hours=9)))

        if now_kst >= datetime(2024, 12, 28, 6, 0, 0, tzinfo=timezone(timedelta(hours=9))):
            color_codes.append("CL_RED_001")

        values_placeholders = ", ".join(["(%s, UNHEX(REPLACE(%s, '-', '')))"] * len(color_codes))
        values = []

        for code in color_codes:
            values.extend([code, user_id])

        query = f"INSERT INTO color (color_code, user_id) VALUES {values_placeholders}"

        await QueryExecutor.execute_write_query(query, tuple(values))

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

from tortoise import fields
from tortoise.models import Model

from app.v2.colors.dtos.color_dto import ColorCodeDTO
from app.v2.colors.querys.color_query import INSERT_COLOR_CODE_FOR_USER_QUERY, SELECT_COLOR_CODE_BY_USER_UUID_QUERY
from common.utils.query_executor import QueryExecutor


class Color(Model):
    color_id = fields.BigIntField(pk=True)  # 자동 증가하는 기본 키
    color_code = fields.CharField(max_length=255, null=True)  # 색상 코드
    user = fields.ForeignKeyField("models.User", related_name="colors", null=True, on_delete=fields.SET_NULL)

    class Meta:
        table = "color"

    @classmethod
    async def get_color_codes_by_user_id(cls, user_id: str) -> list[dict]:
        query = SELECT_COLOR_CODE_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="multiple")

    @classmethod
    async def add_color_code_for_user(cls, user_id: str, color_code: str) -> dict:
        query = INSERT_COLOR_CODE_FOR_USER_QUERY
        values = (color_code, user_id)
        return await QueryExecutor.execute_query(query, values=values, fetch_type="single")

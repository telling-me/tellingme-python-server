from tortoise import fields
from tortoise.models import Model

from app.v2.colors.dtos.color_dto import ColorCodeDTO
from common.query_executor import QueryExecutor


class Color(Model):
    color_id = fields.BigIntField(pk=True)  # 자동 증가하는 기본 키
    color_code = fields.CharField(max_length=255, null=True)  # 색상 코드
    user = fields.ForeignKeyField(
        "models.User", related_name="colors", null=True, on_delete=fields.SET_NULL
    )

    class Meta:
        table = "color"

    @classmethod
    async def get_color_codes_by_user_id(cls, uuid_bytes: bytes) -> list[ColorCodeDTO]:
        hex_data = uuid_bytes.hex()
        query = f"SELECT color_code FROM color WHERE user_id = UNHEX('{hex_data}')"
        colors = await QueryExecutor.execute_query(query, fetch_type="multiple")
        return [ColorCodeDTO(colorCode=color.get("color_code")) for color in colors]

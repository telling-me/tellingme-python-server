from tortoise import Model, fields
from tortoise.transactions import in_transaction

from app.dtos.color.color_data import ColorData


class ColorInventory(Model):
    color_code = fields.CharField(max_length=255, primary_key=True)
    color_name = fields.CharField(max_length=255, null=True)
    color_hex_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "color_inventory"  # 테이블 이름을 명시

    @classmethod
    async def create_bulk(cls) -> None:
        colors = [
            cls(color_code="CL_BLUE_001", color_hex_code="#229DF6", color_name="Blue_1"),
            cls(color_code="CL_DEFAULT", color_hex_code="#1EDCC5", color_name="Default"),
            cls(color_code="CL_GREEN_001", color_hex_code="#80E252", color_name="Green_1"),
            cls(color_code="CL_NAVY_001", color_hex_code="#7075FF", color_name="Navy_1"),
            cls(color_code="CL_ORANGE_001", color_hex_code="#FFA216", color_name="Orange_1"),
            cls(color_code="CL_PINK_001", color_hex_code="#FC6CA0", color_name="Pink_1"),
            cls(color_code="CL_PURPLE_001", color_hex_code="#8C56FF", color_name="Purple_1"),
            cls(color_code="CL_RED_001", color_hex_code="#ED3639", color_name="Red_1"),
            cls(color_code="CL_YELLOW_001", color_hex_code="#FFC543", color_name="Yellow_1"),
        ]
        async with in_transaction():
            await cls.bulk_create(colors)

    @classmethod
    async def get_color_inventory(cls) -> list[ColorData]:
        result = await cls.all().values("color_code", "color_name", "color_hex_code")
        return [ColorData(**row) for row in result]

from tortoise import Model, fields

from app.dtos.color.color_data import ColorData


class ColorInventory(Model):
    color_code = fields.CharField(max_length=255, primary_key=True)
    color_name = fields.CharField(max_length=255, null=True)
    color_hex_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "color_inventory"  # 테이블 이름을 명시

    @classmethod
    async def get_color_inventory(cls) -> list[ColorData]:
        result = await cls.all().values("color_code", "color_name", "color_hex_code")
        return [ColorData(**row) for row in result]

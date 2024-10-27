from app.v2.colors.dtos.color_dto import ColorCodeDTO
from app.v2.colors.models.color import Color


class ColorService:
    @classmethod
    async def get_colors(cls, user_id: str) -> list[ColorCodeDTO]:
        colors_raw = await Color.get_color_codes_by_user_id(user_id=user_id)
        return [ColorCodeDTO.builder(color) for color in colors_raw]

    @classmethod
    async def add_color(cls, user_id: str, color_code: str) -> None:
        await Color.add_color_code_for_user(user_id=user_id, color_code=color_code)

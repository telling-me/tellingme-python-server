from app.dtos.color.color_code_dto import ColorCodeDTO
from app.dtos.color.color_dto import ColorDTO
from app.models.color import Color
from app.models.color_inventory import ColorInventory
from app.models.user import User


class ColorService:
    @classmethod
    async def get_colors(cls, user_id: str) -> list[ColorCodeDTO]:
        colors_raw = await Color.get_color_codes_by_user_id(user_id=user_id)
        return [ColorCodeDTO.builder(color) for color in colors_raw]

    @classmethod
    async def get_colors_with_details_by_user_id(cls, user_id: str) -> list[ColorDTO]:
        user = await User.get_user_profile_by_user_id(user_id=user_id)

        if user.is_premium:
            colors = await ColorInventory.get_color_inventory()
        else:
            colors = await Color.get_colors_with_details_by_user_id(user_id=user_id)

        return [
            ColorDTO(
                colorCode=color.color_code,
                colorName=color.color_name,
                colorHexCode=color.color_hex_code,
            )
            for color in colors
        ]

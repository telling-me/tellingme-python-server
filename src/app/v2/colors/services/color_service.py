from app.v2.colors.dtos.color_dto import ColorCodeDTO, ColorDTO
from app.v2.colors.models.color import Color, ColorInventory
from app.v2.users.services.user_service import UserService


class ColorService:
    @classmethod
    async def get_colors(cls, user_id: str) -> list[ColorCodeDTO]:
        colors_raw = await Color.get_color_codes_by_user_id(user_id=user_id)
        return [ColorCodeDTO.builder(color) for color in colors_raw]

    @classmethod
    async def add_color(cls, user_id: str, color_code: str) -> None:
        await Color.add_color_code_for_user(user_id=user_id, color_code=color_code)

    @classmethod
    async def get_colors_with_details_by_user_id(cls, user_id: str) -> list[ColorDTO]:
        user = await UserService.get_user_profile(user_id=user_id)
        if user.is_premium:
            colors_raw = await ColorInventory.get_color_inventory()
        else:
            colors_raw = await Color.get_colors_with_details_by_user_id(user_id=user_id)

        return [ColorDTO.builder(color) for color in colors_raw]

    @classmethod
    async def get_color_inventory(cls) -> list[dict[str, str]]:
        return await ColorInventory.get_color_inventory()

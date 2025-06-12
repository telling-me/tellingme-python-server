from app.services.color_service import ColorService


class ColorMother:

    @staticmethod
    async def create_color(user_id: str, color_code: str) -> None:
        color_service = ColorService()
        await color_service.create_color(user_id=user_id, color_code=color_code)

    @staticmethod
    async def create_color_inventory() -> None:
        color_service = ColorService()
        await color_service.create_color_inventory()

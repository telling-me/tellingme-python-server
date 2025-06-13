from app.services.color_service import ColorService


class ColorMother:

    @staticmethod
    async def create_color_inventory() -> None:
        color_service = ColorService()
        await color_service.create_color_inventory()

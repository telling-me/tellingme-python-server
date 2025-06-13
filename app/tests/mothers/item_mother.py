import asyncio

from app.services.item_service import ItemService


class ItemMother:

    @staticmethod
    async def create_item_inventory_and_product_inventory() -> None:
        item_service = ItemService()
        await asyncio.gather(
            item_service.create_item_inventory(),
            item_service.create_product_inventory(),
        )
        await item_service.create_link_item_product()

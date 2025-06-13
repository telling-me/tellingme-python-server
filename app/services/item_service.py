from app.models.item import ItemInventory, ItemInventoryProductInventory, ProductInventory


class ItemService:
    @classmethod
    async def create_item_inventory(cls) -> None:
        await ItemInventory.create_bulk()

    @classmethod
    async def create_product_inventory(cls) -> None:
        await ProductInventory.create_bulk()

    @classmethod
    async def create_link_item_product(cls) -> None:
        await ItemInventoryProductInventory.create_bulk()

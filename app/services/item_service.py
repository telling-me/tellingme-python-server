from app.models.item import (
    ItemInventory,
    ItemInventoryProductInventory,
    ItemInventoryRewardInventory,
    ProductInventory,
    RewardInventory,
)


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

    @classmethod
    async def create_reward_inventory(cls) -> None:
        await RewardInventory.create_bulk()

    @classmethod
    async def create_link_item_reward(cls) -> None:
        await ItemInventoryRewardInventory.create_bulk()

from tortoise import Model, fields
from tortoise.transactions import in_transaction


class LevelInventory(Model):
    level_inventory_id = fields.BigIntField(primary_key=True)
    level = fields.IntField(null=True)
    required_exp = fields.IntField(null=True)

    class Meta:
        table = "level_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        levels = [
            cls(level=1, required_exp=15),
            cls(level=2, required_exp=20),
            cls(level=3, required_exp=20),
            cls(level=4, required_exp=20),
            cls(level=5, required_exp=20),
            cls(level=6, required_exp=30),
            cls(level=7, required_exp=30),
            cls(level=8, required_exp=30),
            cls(level=9, required_exp=30),
            cls(level=10, required_exp=30),
            cls(level=11, required_exp=30),
            cls(level=12, required_exp=30),
            cls(level=13, required_exp=30),
            cls(level=14, required_exp=30),
            cls(level=15, required_exp=30),
            cls(level=16, required_exp=30),
            cls(level=17, required_exp=30),
            cls(level=18, required_exp=30),
            cls(level=19, required_exp=30),
            cls(level=20, required_exp=30),
            cls(level=21, required_exp=30),
            cls(level=22, required_exp=30),
        ]

        async with in_transaction():
            await cls.bulk_create(levels)

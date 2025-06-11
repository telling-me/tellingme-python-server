from tortoise import Model, fields


class LevelInventory(Model):
    level_inventory_id = fields.BigIntField(primary_key=True)
    level = fields.IntField(null=True)
    required_exp = fields.IntField(null=True)

from tortoise import fields, models
from tortoise.fields import ForeignKeyRelation


class ItemInventory(models.Model):
    item_id = fields.BigIntField(pk=True)
    item_category = fields.CharField(max_length=255, null=True)
    item_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "item_inventory"


class ProductInventory(models.Model):
    product_id = fields.BigIntField(pk=True)
    price = fields.FloatField(null=True)
    product_category = fields.CharField(max_length=255, null=True)
    product_code = fields.CharField(max_length=255, null=True)
    transaction_currency = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "product_inventory"


class ItemInventoryProductInventory(models.Model):
    item_inventory_product_inventory_id = fields.BigIntField(pk=True)
    quantity = fields.IntField()
    item_inventory: ForeignKeyRelation[ItemInventory] = fields.ForeignKeyField(
        "models.ItemInventory", related_name="product_inventories"
    )
    product_inventory: ForeignKeyRelation[ProductInventory] = fields.ForeignKeyField(
        "models.ProductInventory", related_name="item_inventories"
    )
    item_measurement = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "item_inventory_product_inventory"


class RewardInventory(models.Model):
    reward_inventory_id = fields.BigIntField(pk=True)
    item_code = fields.CharField(max_length=255, null=True)
    reward_code = fields.CharField(max_length=255, null=True)
    reward_description = fields.CharField(max_length=255, null=True)
    reward_name = fields.CharField(max_length=255, null=True)

    item_inventories = fields.ReverseRelation["ItemInventoryRewardInventory"]

    class Meta:
        table = "reward_inventory"


class ItemInventoryRewardInventory(models.Model):
    item_inventory_reward_invnetory_id = fields.BigIntField(pk=True)
    quantity = fields.IntField()
    item_inventory: ForeignKeyRelation[ItemInventory] = fields.ForeignKeyField(
        "models.ItemInventory",
        related_name="reward_inventories",
        on_delete=fields.CASCADE,
        db_column="item_inventory_id",
    )
    reward_inventory: ForeignKeyRelation[RewardInventory] = fields.ForeignKeyField(
        "models.RewardInventory",
        related_name="item_inventories",
        on_delete=fields.CASCADE,
        db_column="reward_inventory_id",
    )
    item_measurement = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "item_inventory_reward_inventory"

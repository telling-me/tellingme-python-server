from tortoise import fields, models


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
    item_inventory = fields.ForeignKeyField(
        "models.ItemInventory", related_name="product_inventories"
    )
    product_inventory = fields.ForeignKeyField(
        "models.ProductInventory", related_name="item_inventories"
    )
    item_measurement = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "item_inventory_product_inventory"

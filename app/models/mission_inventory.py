from tortoise import Model, fields


class MissionInventory(Model):
    mission_inventory_id = fields.BigIntField(primary_key=True)
    condition_type = fields.CharField(max_length=255)
    mission_code = fields.CharField(max_length=255)
    mission_description = fields.CharField(max_length=255)
    mission_name = fields.CharField(max_length=255)
    reward_code = fields.CharField(max_length=255)
    target_count = fields.IntField()

    class Meta:
        table = "mission_inventory"

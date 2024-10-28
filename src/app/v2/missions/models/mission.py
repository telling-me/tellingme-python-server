from tortoise import fields
from tortoise.models import Model


class UserMission(Model):
    user_mission_id = fields.BigIntField(pk=True)
    is_completed = fields.BooleanField(default=False)
    mission_code = fields.CharField(max_length=255)
    progress_count = fields.IntField(default=0)
    user = fields.ForeignKeyField("models.User", related_name="missions")


class MissionInventory(Model):
    mission_inventory_id = fields.BigIntField(pk=True)
    condition_type = fields.CharField(max_length=255)
    mission_code = fields.CharField(max_length=255)
    mission_description = fields.CharField(max_length=255)
    mission_name = fields.CharField(max_length=255)
    reward_code = fields.CharField(max_length=255)
    target_count = fields.IntField()

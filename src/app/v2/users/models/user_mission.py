from tortoise import fields
from tortoise.models import Model


class UserMission(Model):
    user_mission_id = fields.BigIntField(pk=True)
    is_completed = fields.BooleanField(null=True)
    mission_code = fields.CharField(max_length=255, null=True)
    progress_count = fields.IntField(null=True)
    user_id = fields.ForeignKeyField("models.User", related_name="missions", null=True)

    class Meta:
        table = "user_mission"

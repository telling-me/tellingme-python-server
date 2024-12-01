from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.users.models.user import User


class UserMission(Model):
    user_mission_id = fields.BigIntField(pk=True)
    is_completed = fields.BooleanField(null=True)
    mission_code = fields.CharField(max_length=255, null=True)
    progress_count = fields.IntField(null=True)
    user: ForeignKeyRelation[User] = fields.ForeignKeyField("models.User", related_name="missions")

    class Meta:
        table = "user_mission"

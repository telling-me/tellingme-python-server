from tortoise import fields
from tortoise.models import Model


class RefreshToken(Model):
    refresh_token_id = fields.BigIntField(primary_key=True)
    access_token = fields.CharField(max_length=255)
    refresh_token = fields.CharField(max_length=255)
    user_id = fields.BinaryField(max_length=16)

    class Meta:
        table = "refresh_token"

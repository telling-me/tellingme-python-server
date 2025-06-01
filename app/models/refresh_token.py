from tortoise import fields
from tortoise.models import Model


class RefreshToken(Model):
    refresh_token_id = fields.BigIntField(pk=True)
    access_token = fields.CharField(max_length=255)
    refresh_token = fields.CharField(max_length=255)
    user_id = fields.BinaryField(max_length=16)  # foreign key로 사용되지는 않지만 binary field로 선언

    class Meta:
        table = "refresh_token"

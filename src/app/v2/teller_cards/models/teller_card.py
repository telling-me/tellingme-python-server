from tortoise import fields
from tortoise.models import Model


class TellerCard(Model):
    teller_card_id = fields.BigIntField(pk=True)
    activate_badge_code = fields.CharField(max_length=255, null=True)
    activate_color_code = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "teller_card"

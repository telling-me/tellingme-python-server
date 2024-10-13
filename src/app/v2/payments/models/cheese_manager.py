from tortoise import fields
from tortoise.models import Model


class CheeseManager(Model):
    cheese_manager_id = fields.BigIntField(pk=True)

    class Meta:
        table = "cheese_manager"

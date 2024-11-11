# models.py
from tortoise import fields
from tortoise.models import Model


# models.py (계속)
class PurchaseHistory(Model):
    purchase_history_id = fields.BigIntField(pk=True)
    product_code = fields.CharField(max_length=255)
    status = fields.CharField(max_length=255)
    receipt_id = fields.CharField(max_length=255, unique=True)  # 영수증 중복 방지
    user = fields.ForeignKeyField("models.User", related_name="purchase_histories")

    class Meta:
        table = "purchase_history"
        unique_together = ("receipt_id",)
        indexes = ["user_id"]

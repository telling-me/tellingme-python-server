from datetime import datetime
from typing import Optional

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.purchases.models.purchase_status import PurchaseStatus, SubscriptionStatus
from app.v2.users.models.user import User
from common.utils.query_executor import QueryExecutor


class Subscription(Model):
    subscription_id = fields.BigIntField(pk=True, description="Primary key for the Subscription")
    product_code = fields.CharField(max_length=255, null=False, description="Product code of the subscription")
    status = fields.CharField(max_length=255, null=False, description="Status of the subscription")
    current_transaction_id = fields.CharField(max_length=255, null=False, description="Current transaction ID")
    expires_date = fields.DatetimeField(null=False, description="Expiration date of the subscription")
    created_at = fields.DatetimeField(auto_now_add=True, description="When the subscription was created")
    updated_at = fields.DatetimeField(auto_now=True, description="Last updated timestamp")

    user: ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User",
        related_name="subscriptions",
        on_delete=fields.CASCADE,
        description="User linked to the subscription",
    )
    purchase_histories = fields.ReverseRelation["PurchaseHistory"]

    class Meta:
        table = "subscription"

    @classmethod
    async def get_subscription_by_user_id_and_product_code(
        cls, user_id: str, product_code: str
    ) -> Optional["Subscription"]:
        query = """
            SELECT * FROM subscription
            WHERE user_id = UNHEX(REPLACE(%s, '-', '')) AND product_code = %s
            LIMIT 1;
        """
        values = (user_id, product_code)

        result = await QueryExecutor.execute_query(query, values=values, fetch_type="single")

        if result:
            return cls(**result)
        return None

    @classmethod
    async def create_or_update_subscription(
        cls,
        user_id: str,
        product_code: str,
        transaction_id: str,
        expires_date_ms: int,
        status: str,
    ) -> "Subscription":
        query = """
                INSERT INTO subscription (user_id, product_code, status, current_transaction_id, expires_date)
                VALUES (UNHEX(REPLACE(%s, '-', '')), %s, %s, %s, FROM_UNIXTIME(%s / 1000))
                ON DUPLICATE KEY UPDATE
                    current_transaction_id = VALUES(current_transaction_id),
                    expires_date = VALUES(expires_date),
                    status = VALUES(status);
            """
        values = (user_id, product_code, status, transaction_id, expires_date_ms)

        await QueryExecutor.execute_query(query, values=values, fetch_type="none")

        return cls(
            user_id=user_id,
            product_code=product_code,
            status=status,
            current_transaction_id=transaction_id,
            expires_date=datetime.fromtimestamp(expires_date_ms / 1000),
        )

    @classmethod
    async def update_subscription(
        cls, user_id: str, product_code: str, transaction_id: str, expires_date_ms: int
    ) -> None:
        expires_date = datetime.fromtimestamp(expires_date_ms / 1000.0)

        query = """
            UPDATE subscription
            SET current_transaction_id = %s,
                expires_date = FROM_UNIXTIME(%s / 1000),
                status = %s
            WHERE user_id = UNHEX(REPLACE(%s, '-', ''))
              AND product_code = %s;
        """
        values = (transaction_id, expires_date_ms, "active", user_id, product_code)

        await QueryExecutor.execute_query(query, values=values, fetch_type="single")


class PurchaseHistory(Model):
    purchase_history_id = fields.BigIntField(pk=True, description="Primary key for the Purchase History")
    product_code = fields.CharField(max_length=255, null=False, description="Product code of the purchase")
    transaction_id = fields.CharField(max_length=255, unique=True, null=False, description="Transaction ID")
    original_transaction_id = fields.CharField(max_length=255, null=True, description="Original transaction ID")
    status = fields.CharField(max_length=255, null=False, description="Purchase status")
    expires_date = fields.DatetimeField(null=True, description="Expiration date of the purchase")
    purchase_date = fields.DatetimeField(null=False, description="Date of the purchase")
    quantity = fields.IntField(default=1, description="Quantity of items purchased")
    is_refunded = fields.BooleanField(default=False, description="Whether the purchase was refunded")
    refunded_at = fields.DatetimeField(null=True, description="When the purchase was refunded")
    receipt_data = fields.TextField(null=True, description="Raw receipt data from Apple")
    created_at = fields.DatetimeField(auto_now_add=True, description="When the purchase was made")
    updated_at = fields.DatetimeField(auto_now=True, description="Last updated timestamp")

    user: ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User",
        related_name="purchase_histories",
        on_delete=fields.CASCADE,
        description="User linked to the purchase",
    )

    subscription: Optional[ForeignKeyRelation["Subscription"]] = fields.ForeignKeyField(
        "models.Subscription",
        related_name="purchase_histories",
        null=True,
        on_delete=fields.SET_NULL,
        description="Linked subscription",
    )

    class Meta:
        table = "purchase_history"

    @classmethod
    async def create_purchase_history(
        cls,
        user_id: str,
        subscription_id: Optional[int],
        product_code: str,
        transaction_id: str,
        original_transaction_id: str,
        status: str,
        expires_date_ms: Optional[int],
        purchase_date_ms: int,
        receipt_data: str,
        quantity: int = 1,
        is_refunded: bool = False,
        refunded_at: Optional[datetime] = None,
    ) -> None:
        query = """
                INSERT INTO purchase_history (
                    user_id, subscription_id, product_code, transaction_id, 
                    original_transaction_id, status, expires_date, purchase_date, 
                    quantity, is_refunded, refunded_at, receipt_data, created_at, updated_at
                )
                VALUES (
                    UNHEX(REPLACE(%s, '-', '')), %s, %s, %s, 
                    %s, %s, FROM_UNIXTIME(%s / 1000), FROM_UNIXTIME(%s / 1000), 
                    %s, %s, %s, %s, NOW(), NOW()
                );
            """

        values = (
            user_id,
            subscription_id,
            product_code,
            transaction_id,
            original_transaction_id,
            status,
            expires_date_ms,
            purchase_date_ms,
            quantity,
            is_refunded,
            refunded_at,
            receipt_data,
        )

        await QueryExecutor.execute_query(query, values=values, fetch_type="single")

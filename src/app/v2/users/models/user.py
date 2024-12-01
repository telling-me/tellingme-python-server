from datetime import datetime
from typing import Any, Optional

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.cheese_managers.models.cheese_manager import CheeseManager
from app.v2.levels.models.level import Level
from app.v2.teller_cards.models.teller_card import TellerCard
from app.v2.users.models.refresh_token import RefreshToken
from app.v2.users.querys.user_query import (
    SELECT_USER_INFO_BY_USER_UUID_QUERY,
    SELECT_USER_PROFILE_BY_USER_ID_QUERY,
    UPDATE_PREMIUM_STATUS_QUERY,
)
from common.utils.query_executor import QueryExecutor


class User(Model):
    user_id = fields.CharField(max_length=255, pk=True, description="Primary key for the User")
    allow_notification = fields.BooleanField(null=True)
    birth_date = fields.CharField(max_length=8, null=True)
    created_time = fields.DatetimeField(auto_now_add=True)
    gender = fields.CharField(max_length=16, null=True)
    job = fields.IntField()
    mbti = fields.CharField(max_length=8, null=True)
    nickname = fields.CharField(max_length=16)
    purpose = fields.CharField(max_length=16)
    push_token = fields.CharField(max_length=255, null=True)
    social_id = fields.CharField(max_length=255)
    social_login_type = fields.CharField(max_length=16)
    user_status = fields.BooleanField()
    withdraw_period = fields.DatetimeField(null=True)
    refresh_token: Optional[ForeignKeyRelation[RefreshToken]] = fields.ForeignKeyField(
        "models.RefreshToken",
        related_name="users",
        db_column="refresh_token_id",
        null=True,
    )
    is_premium = fields.BooleanField()
    profile_url = fields.CharField(
        max_length=255,
        default="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*dh7Xy5tFvRj7n2wf1UweAw.png",
    )
    premium_started_at = fields.DatetimeField(null=True)
    cheese_manager: ForeignKeyRelation[CheeseManager] = fields.ForeignKeyField(
        "models.CheeseManager",
        related_name="users",
        db_column="cheese_manager_id",
    )
    teller_card: ForeignKeyRelation[TellerCard] = fields.ForeignKeyField(
        "models.TellerCard",
        related_name="users",
        db_column="teller_card_id",
    )
    level: ForeignKeyRelation[Level] = fields.ForeignKeyField(
        "models.Level",
        related_name="users",
        db_column="level_id",
    )

    class Meta:
        table = "user"

    @classmethod
    async def get_user_profile_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_USER_PROFILE_BY_USER_ID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="single")

    @classmethod
    async def get_user_info_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_USER_INFO_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="single")

    @classmethod
    async def set_is_premium(cls, user_id: str, is_premium: bool) -> Any:
        query = UPDATE_PREMIUM_STATUS_QUERY
        current_time = datetime.now()
        values = (int(is_premium), current_time, user_id)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")

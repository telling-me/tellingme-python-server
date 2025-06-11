import uuid
from datetime import datetime
from typing import Any, Optional

from tortoise import Tortoise, fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.dtos.user.user_data import UserData
from app.dtos.user.user_dto import UserProfileData
from app.models.cheese_manager import CheeseManager
from app.models.level import Level
from app.models.refresh_token import RefreshToken
from app.models.teller_card import TellerCard
from app.queries.user_query import (
    SELECT_USER_INFO_BY_USER_UUID_QUERY,
    SELECT_USER_PROFILE_BY_USER_ID_QUERY,
    UPDATE_PREMIUM_STATUS_QUERY,
)


class User(Model):
    user_id = fields.CharField(max_length=255, primary_key=True, description="Primary key for the User")
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
    async def get_user_profile_by_user_id(cls, user_id: str) -> UserProfileData:
        query = SELECT_USER_PROFILE_BY_USER_ID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return UserProfileData(
            user_id=result.get("user_id", ""),
            nickname=result.get("nickname", ""),
            profile_url=result.get("profile_url", ""),
            is_premium=result.get("is_premium") != b"\x00",
            user_status=result.get("user_status") != b"\x00",
            cheese_manager_id=result.get("cheese_manager_id", 0),
            teller_card_id=result.get("teller_card_id", 0),
            level_id=result.get("level_id", 0),
            allow_notification=result.get("allow_notification") != b"\x00",
        )

    @classmethod
    async def get_user_info_by_user_id(cls, user_id: str) -> UserData:
        query = SELECT_USER_INFO_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return UserData(**result)

    @classmethod
    async def set_is_premium(cls, user_id: str, is_premium: bool) -> None:
        query = UPDATE_PREMIUM_STATUS_QUERY
        current_time = datetime.now()
        values = (int(is_premium), current_time, user_id)
        await QueryExecutor.execute_query(query, values=values, fetch_type="single")

    @classmethod
    def format_user_id(cls, user_id_bytes: bytes) -> str:
        return str(uuid.UUID(bytes=user_id_bytes))

    @classmethod
    def format_user_ids(cls, user_ids: list[bytes]) -> str:
        return ", ".join([f"UNHEX(REPLACE('{str(uuid.UUID(bytes=user_id))}', '-', ''))" for user_id in user_ids])

    @classmethod
    async def bulk_update_is_premium(cls, user_ids: list[bytes]) -> None:
        query = f"""
            UPDATE user
            SET is_premium = FALSE
            WHERE user_id IN ({cls.format_user_ids(user_ids)});
        """
        await Tortoise.get_connection("default").execute_query(query)

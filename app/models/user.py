from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from tortoise import Tortoise, fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.core.configs import settings
from app.dtos.user.user_data import UserData
from app.dtos.user.user_dto import UserProfileData
from app.models.refresh_token import RefreshToken
from app.queries.user_query import (
    SELECT_USER_INFO_BY_USER_UUID_QUERY,
    SELECT_USER_PROFILE_BY_USER_ID_QUERY,
    UPDATE_PREMIUM_STATUS_QUERY,
)


class User(Model):
    id = fields.BigIntField(primary_key=True)  # Auto Increment Primary Key
    user_id = fields.BinaryField(max_length=16, description="UUID PK in binary form")
    allow_notification = fields.BinaryField(null=True)
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
    user_status = fields.BinaryField()
    withdraw_period = fields.DatetimeField(null=True)
    refresh_token: Optional[ForeignKeyRelation[RefreshToken]] = fields.ForeignKeyField(
        "models.RefreshToken",
        related_name="users",
        db_column="refresh_token_id",
        null=True,
    )
    is_premium = fields.BinaryField()
    profile_url = fields.CharField(
        max_length=255,
        default="https://miro.medium.com/v2/resize:fit:1400/format:webp/1*dh7Xy5tFvRj7n2wf1UweAw.png",
    )
    premium_started_at = fields.DatetimeField(null=True)
    cheese_manager_id = fields.BigIntField(null=True)
    teller_card_id = fields.BigIntField(null=True)
    level_id = fields.BigIntField(null=True)

    class Meta:
        table = "user"

    @classmethod
    async def create_user(
        cls,
        social_id: str,
        social_login_type: str,
        nickname: str,
        purpose: str,
        job: int,
        cheese_manager_id: int,
        teller_card_id: int,
        level_id: int,
        allow_notification: bool = False,
        birth_date: str | None = None,
        gender: str = "female",
        mbti: str | None = None,
        push_token: str | None = None,
        refresh_token: RefreshToken | None = None,
        is_premium: bool = False,
        profile_url: str | None = "",
    ) -> str:

        user_id = str(uuid.uuid4())
        created_time = datetime.now(settings.db_zoneinfo).strftime("%Y-%m-%d %H:%M:%S")
        allow_notification_byte = b"\x01" if allow_notification else b"\x00"
        is_premium_byte = b"\x01" if is_premium else b"\x00"
        user_status_byte = b"\x01"  # 항상 TRUE로 설정한 부분

        query = """
                INSERT INTO user (
                    user_id, social_id, social_login_type, nickname, purpose, job,
                    cheese_manager_id, teller_card_id, level_id,
                    allow_notification, birth_date, gender, mbti,
                    push_token, refresh_token_id, is_premium, profile_url, user_status, created_time
                )
                VALUES (
                    UNHEX(REPLACE(%s, '-', '')), %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                );
                """

        await QueryExecutor.execute_write_query(
            query,
            (
                user_id,
                social_id,
                social_login_type,
                nickname,
                purpose,
                job,
                cheese_manager_id,
                teller_card_id,
                level_id,
                allow_notification_byte,
                birth_date,
                gender,
                mbti,
                push_token,
                refresh_token,
                is_premium_byte,
                profile_url,
                user_status_byte,
                created_time,
            ),
        )
        return user_id

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

    @staticmethod
    def uuid_str_to_bytes(s: str) -> bytes:
        return uuid.UUID(s).bytes

    @staticmethod
    def uuid_bytes_to_str(b: bytes) -> str:
        return str(uuid.UUID(bytes=b))

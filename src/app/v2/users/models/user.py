from tortoise import fields
from tortoise.models import Model

from app.v2.levels.dtos.level_dto import LevelDTO
from app.v2.teller_cards.dtos.teller_card_dto import TellerCardDTO
from app.v2.users.dtos.user_info_dto import UserInfoDTO
from app.v2.users.querys.user_query import (
    SELECT_USER_BY_UUID_QUERY,
    SELECT_USER_INFO_BY_USER_UUID_QUERY,
    SELECT_USER_LEVEL_AND_EXP_BY_USER_UUID_QUERY,
)
from common.utils.query_executor import QueryExecutor
from common.utils.query_formatter import QueryFormatter


class User(Model):
    user_id = fields.BinaryField(pk=True)  # BINARY(16)로 저장
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
    refresh_token = fields.ForeignKeyField(
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
    user_exp = fields.IntField(null=True)
    user_level = fields.IntField(null=True)
    cheese_manager = fields.ForeignKeyField(
        "models.CheeseManager",
        related_name="users",
        db_column="cheese_manager_id",
        null=True,
    )
    teller_card = fields.ForeignKeyField(
        "models.TellerCard",
        related_name="users",
        db_column="teller_card_id",
        null=True,
    )

    class Meta:
        table = "user"

    @classmethod
    async def get_by_user_id(cls, user_id: str) -> "User":
        query = QueryFormatter.format(
            query_template=SELECT_USER_BY_UUID_QUERY, values=user_id
        )
        users = await cls.raw(query)
        if users:
            return users[0]  # 첫 번째 결과 반환
        return None

    @classmethod
    async def get_user_info_by_user_id(cls, user_id: str) -> dict | None:
        query = SELECT_USER_INFO_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(
            query, values=value, fetch_type="single"
        )
        return result[0] if result else None

    @classmethod
    async def get_level_info_by_user_id(cls, user_id: str) -> dict | None:
        query = SELECT_USER_LEVEL_AND_EXP_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(
            query, values=value, fetch_type="multiple"
        )
        return result[0] if result else None

from datetime import datetime
from typing import Any

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.answers.querys.answer_query import (
    SELECT_ANSWER_BY_USER_UUID_QUERY,
    SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY,
    SELECT_MOST_RECENT_ANSWER_BY_USER_UUID_QUERY,
    SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY_V2,
)
from app.v2.users.models.user import User
from common.utils.query_executor import QueryExecutor


class Answer(Model):
    answer_id = fields.BigIntField(pk=True)
    content = fields.TextField(null=False)
    created_time = fields.DatetimeField(null=True)
    date = fields.DateField(null=False)
    emotion = fields.IntField(null=False)
    is_premium = fields.BooleanField(null=False)
    is_public = fields.BooleanField(null=False)
    modified_time = fields.DatetimeField(null=True)
    is_blind = fields.BooleanField(null=False)
    blind_ended_at = fields.DatetimeField(null=True)
    blind_started_at = fields.DatetimeField(null=True)
    like_count = fields.IntField(null=False, default=0)
    is_spare = fields.BooleanField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    user: ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="answers", on_delete=fields.CASCADE
    )

    class Meta:
        table = "answer"

    # 기존 get_answer_count_by_user_id 메서드
    @classmethod
    async def get_answer_count_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="single")

    @classmethod
    async def get_answer_count_by_user_id_v2(cls, user_id: str) -> Any:
        query = SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY_V2
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="single")

    @classmethod
    async def find_all_by_user(cls, user_id: str, start_date: datetime, end_date: datetime) -> Any:
        query = SELECT_ANSWER_BY_USER_UUID_QUERY
        values = (user_id, start_date, end_date)
        return await QueryExecutor.execute_query(query, values=values, fetch_type="multiple")

    @classmethod
    async def get_most_recent_answer_by_user_id(cls, user_id: str) -> Any:
        query = SELECT_MOST_RECENT_ANSWER_BY_USER_UUID_QUERY
        value = user_id
        return await QueryExecutor.execute_query(query, values=value, fetch_type="single")

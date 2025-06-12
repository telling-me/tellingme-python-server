from datetime import datetime

from tortoise import fields
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.core.configs import settings
from app.dtos.answer.answer_data import AnswerData
from app.queries.answer_query import (
    SELECT_ANSWER_BY_USER_UUID_QUERY,
    SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY,
    SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY_V2,
    SELECT_MOST_RECENT_ANSWER_BY_USER_UUID_QUERY,
)


class Answer(Model):
    answer_id = fields.BigIntField(primary_key=True)
    user_id = fields.BinaryField(max_length=16, null=True)
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

    class Meta:
        table = "answer"

    @classmethod
    async def create_answer(
        cls,
        user_id: str,
        content: str,
        date: str,
        emotion: int = 1,
        like_count: int = 0,
        is_premium: bool = False,
        is_public: bool = False,
        is_blind: bool = False,
        is_spare: bool = False,
    ) -> None:
        created_time = datetime.now(settings.db_zoneinfo).strftime("%Y-%m-%d %H:%M:%S")

        query = """
                INSERT INTO answer (
                    user_id, content, date, emotion,
                    is_premium, is_public, is_blind, is_spare,
                    created_time, like_count
                )
                VALUES (
                    UNHEX(REPLACE(%s, '-', '')), %s, %s, %s,
                    %s, %s, %s, %s,
                    %s, %s
                );
            """

        await QueryExecutor.execute_write_query(
            query,
            (user_id, content, date, emotion, is_premium, is_public, is_blind, is_spare, created_time, like_count),
        )

    # 기존 get_answer_count_by_user_id 메서드
    @classmethod
    async def get_answer_count_by_user_id(cls, user_id: str) -> int:
        query = SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return int(result.get("answer_count", 0) if result else 0)

    @classmethod
    async def get_answer_count_by_user_id_v2(cls, user_id: str) -> int:
        query = SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY_V2
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return int(result.get("answer_count", 0) if result else 0)

    @classmethod
    async def get_all_by_user_id(cls, user_id: str, start_date: datetime, end_date: datetime) -> list[AnswerData]:
        query = SELECT_ANSWER_BY_USER_UUID_QUERY
        values = (user_id, start_date, end_date)
        results = await QueryExecutor.execute_query(query, values=values, fetch_type="multiple")
        return [AnswerData(**row) for row in results]

    @classmethod
    async def get_most_recent_answer_by_user_id(cls, user_id: str) -> AnswerData | None:
        query = SELECT_MOST_RECENT_ANSWER_BY_USER_UUID_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return AnswerData(**result) if result else None

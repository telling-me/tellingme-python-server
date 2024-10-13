from fastapi import Depends
from tortoise import fields, Tortoise
from tortoise.models import Model

from common.query_executor import QueryExecutor


class Answer(Model):
    answer_id = fields.BigIntField(pk=True)
    content = fields.TextField(null=False)
    created_time = fields.DatetimeField(null=True)
    date = fields.DateField(null=False)
    emotion = fields.IntField(null=False)
    is_premium = fields.BooleanField(null=False)
    is_public = fields.BooleanField(null=False)
    modified_time = fields.DatetimeField(null=True)
    user = fields.ForeignKeyField(
        "models.User", related_name="answers", null=True, on_delete=fields.SET_NULL
    )  # 외래 키 정의
    is_blind = fields.BooleanField(null=False)
    blind_ended_at = fields.DatetimeField(null=True)
    blind_started_at = fields.DatetimeField(null=True)
    like_count = fields.IntField(null=False, default=0)
    is_spare = fields.BooleanField(null=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "answer"

    @classmethod
    async def get_answer_count_by_user_id(
        cls,
        uuid_bytes: bytes,
    ) -> int:
        hex_data = uuid_bytes.hex()  # uuid_bytes를 16진수 문자열로 변환
        query = (
            f"SELECT COUNT(*) as answer_count FROM answer WHERE user_id = 0x{hex_data}"
        )
        return await QueryExecutor.execute_query(query, fetch_type="single")

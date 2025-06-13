from tortoise import fields
from tortoise.models import Model

from app.common.utils.query_executor import QueryExecutor
from app.queries.like_query import SELECT_UNIQUE_LIKES_COUNT_BY_USER_TODAY_QUERY


class Like(Model):
    likes_id = fields.BigIntField(primary_key=True)
    answer_id = fields.BinaryField(null=True)
    user_id = fields.BinaryField(max_length=16, null=True)
    created_time = fields.DatetimeField(null=True)
    modified_time = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "likes"

    @staticmethod
    async def get_unique_likes_today(user_id: str) -> int:
        query = SELECT_UNIQUE_LIKES_COUNT_BY_USER_TODAY_QUERY
        value = user_id
        result = await QueryExecutor.execute_query(query, values=value, fetch_type="single")
        return int(result.get("unique_likes", 0) if result else 0)

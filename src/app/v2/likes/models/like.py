from typing import Any

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.answers.models.answer import Answer
from app.v2.likes.querys.like_query import SELECT_UNIQUE_LIKES_COUNT_BY_USER_TODAY_QUERY
from app.v2.users.models.user import User
from common.utils.query_executor import QueryExecutor


class Like(Model):
    likes_id = fields.BigIntField(pk=True)
    answer: ForeignKeyRelation[Answer] = fields.ForeignKeyField(
        "models.Answer", related_name="likes", on_delete=fields.CASCADE
    )
    user: ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="likes", on_delete=fields.CASCADE
    )
    created_time = fields.DatetimeField(null=True)
    modified_time = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "likes"
        indexes = [
            ("answer_id",),
            ("user_id",),
        ]

    @staticmethod
    async def get_unique_likes_today(user_id: str) -> Any:
        query = SELECT_UNIQUE_LIKES_COUNT_BY_USER_TODAY_QUERY
        values = (user_id,)
        return await QueryExecutor.execute_query(query, values=values, fetch_type="single")

from tortoise import fields
from tortoise.fields import ForeignKeyRelation
from tortoise.models import Model

from app.v2.users.models.user import User
from common.utils.query_executor import QueryExecutor


class Notice(Model):
    notice_id = fields.BigIntField(pk=True)
    title = fields.CharField(max_length=255, null=False)
    content = fields.TextField(null=True)
    is_read = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    link = fields.CharField(max_length=255, null=True)
    is_internal = fields.BooleanField(default=False)
    answer_id = fields.BigIntField(null=True)
    date = fields.DateField(null=True)
    reward_type = fields.CharField(max_length=255, null=True)

    user: ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="notices", null=True, on_delete=fields.SET_NULL
    )

    class Meta:
        table = "notice"

    @classmethod
    async def create_notice(
        cls,
        title: str,
        content: str,
        user_id: int,
        link: str = None,
        is_read: bool = False,
        is_internal: bool = False,
        answer_id: int = None,
        date: str = None,
        reward_type: str = None,
    ) -> None:
        query = """
                    INSERT INTO notice (
                        title, content, user_id, link, is_internal, is_read, answer_id, date, reward_type,
                        created_at
                    )
                    VALUES (
                        %s, %s, UNHEX(REPLACE(%s, '-', '')), %s, %s, %s, %s, %s, %s, NOW()
                    );
                """
        values = (title, content, user_id, link, is_internal, is_read, answer_id, date, reward_type)

        await QueryExecutor.execute_query(query, values=values, fetch_type="single")

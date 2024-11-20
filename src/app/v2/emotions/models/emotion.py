from tortoise import fields, models

from app.v2.emotions.querys.emotion_query import (
    INSERT_EMOTION_CODE_FOR_USER_QUERY,
    SELECT_EMOTION_CODE_BY_USER_UUID_QUERY,
)
from common.utils.query_executor import QueryExecutor


class Emotion(models.Model):
    emotion_id = fields.BigIntField(pk=True)
    emotion_code = fields.CharField(max_length=255, unique=True)
    user = fields.ForeignKeyField("models.User", related_name="emotions")

    class Meta:
        table = "emotion"

    @classmethod
    async def get_emotions_with_details_by_user_id(cls, user_id: str) -> list[dict]:
        query = SELECT_EMOTION_CODE_BY_USER_UUID_QUERY
        values = user_id
        return await QueryExecutor.execute_query(query, values=values, fetch_type="multiple")

    @classmethod
    async def add_emotion(cls, user_id: str, emotion_code: str) -> None:
        query = INSERT_EMOTION_CODE_FOR_USER_QUERY
        values = (emotion_code, user_id)
        await QueryExecutor.execute_query(query, values=values)


class EmotionInventory(models.Model):
    emotion_inventory_id = fields.BigIntField(pk=True)
    emotion_code = fields.CharField(max_length=255, unique=True)
    emotion_name = fields.CharField(max_length=255)

    class Meta:
        table = "emotion_inventory"

    @classmethod
    async def get_emotion_inventory(cls) -> list[dict]:
        return await cls.all().values("emotion_code", "emotion_name")

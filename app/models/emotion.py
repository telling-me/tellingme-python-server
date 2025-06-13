from tortoise import fields, models

from app.common.utils.query_executor import QueryExecutor
from app.dtos.emotion.emotion_data import EmotionData
from app.queries.emotion_query import (
    INSERT_EMOTION_CODE_FOR_USER_QUERY,
    SELECT_EMOTION_CODE_BY_USER_UUID_QUERY,
)


class Emotion(models.Model):
    emotion_id = fields.BigIntField(primary_key=True)
    emotion_code = fields.CharField(max_length=255)
    user_id = fields.BinaryField(max_length=16, null=True)

    class Meta:
        table = "emotion"

    @classmethod
    async def create_default_emotions_by_user_id(cls, user_id: str) -> None:
        emotion_codes = ["EM_HAPPY", "EM_PROUD", "EM_OKAY", "EM_TIRED", "EM_SAD", "EM_ANGRY"]

        values_placeholders = ", ".join(["(%s, UNHEX(REPLACE(%s, '-', '')))"] * len(emotion_codes))
        values = []

        for code in emotion_codes:
            values.extend([code, user_id])

        query = f"INSERT INTO emotion (emotion_code, user_id) VALUES {values_placeholders}"

        await QueryExecutor.execute_write_query(query, tuple(values))

    @classmethod
    async def create_by_user_id(cls, user_id: str, emotion_code: str) -> None:
        query = INSERT_EMOTION_CODE_FOR_USER_QUERY
        values = (emotion_code, user_id)
        await QueryExecutor.execute_query(query, values=values)

    @classmethod
    async def get_emotions_with_details_by_user_id(cls, user_id: str) -> list[EmotionData]:
        query = SELECT_EMOTION_CODE_BY_USER_UUID_QUERY
        values = user_id
        result = await QueryExecutor.execute_query(query, values=values, fetch_type="multiple")
        return [EmotionData(**row) for row in result]

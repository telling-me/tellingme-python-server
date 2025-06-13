from tortoise import fields, models
from tortoise.transactions import in_transaction

from app.dtos.emotion.emotion_data import EmotionData


class EmotionInventory(models.Model):
    emotion_inventory_id = fields.BigIntField(primary_key=True)
    emotion_code = fields.CharField(max_length=255, unique=True)
    emotion_name = fields.CharField(max_length=255)

    class Meta:
        table = "emotion_inventory"

    @classmethod
    async def create_bulk(cls) -> None:
        emotions = [
            cls(emotion_code="EM_HAPPY", emotion_name="행복해요"),
            cls(emotion_code="EM_PROUD", emotion_name="뿌듯해요"),
            cls(emotion_code="EM_OKAY", emotion_name="그저 그래요"),
            cls(emotion_code="EM_TIRED", emotion_name="피곤해요"),
            cls(emotion_code="EM_SAD", emotion_name="슬퍼요"),
            cls(emotion_code="EM_ANGRY", emotion_name="화나요"),
            cls(emotion_code="EM_EXCITED", emotion_name="설레요"),
            cls(emotion_code="EM_FUN", emotion_name="신나요"),
            cls(emotion_code="EM_RELAXED", emotion_name="편안해요"),
            cls(emotion_code="EM_APATHETIC", emotion_name="무기력해요"),
            cls(emotion_code="EM_LONELY", emotion_name="외로워요"),
            cls(emotion_code="EM_COMPLEX", emotion_name="복잡해요"),
        ]
        async with in_transaction():
            await cls.bulk_create(emotions)

    @classmethod
    async def get_emotion_inventory(cls) -> list[EmotionData]:
        result = await cls.all().values("emotion_code", "emotion_name")
        return [EmotionData(**row) for row in result]

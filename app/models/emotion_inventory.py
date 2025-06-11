from tortoise import fields, models

from app.dtos.emotion.emotion_data import EmotionData


class EmotionInventory(models.Model):
    emotion_inventory_id = fields.BigIntField(primary_key=True)
    emotion_code = fields.CharField(max_length=255, unique=True)
    emotion_name = fields.CharField(max_length=255)

    class Meta:
        table = "emotion_inventory"

    @classmethod
    async def get_emotion_inventory(cls) -> list[EmotionData]:
        result = await cls.all().values("emotion_code", "emotion_name")
        return [EmotionData(**row) for row in result]

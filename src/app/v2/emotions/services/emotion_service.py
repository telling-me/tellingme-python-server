from app.v2.emotions.models.emotion import Emotion, EmotionInventory


class EmotionService:
    @classmethod
    async def get_emotions(cls, user_id: str) -> list[dict]:
        return await Emotion.get_emotions_with_details_by_user_id(user_id=user_id)

    @classmethod
    async def add_emotion(cls, user_id: str, emotion_code: str) -> None:
        await Emotion.add_emotion(user_id=user_id, emotion_code=emotion_code)

    @classmethod
    async def get_emotion_inventory(cls) -> list[dict]:
        return await EmotionInventory.get_emotion_inventory()

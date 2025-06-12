from app.services.emotion_service import EmotionService


class EmotionMother:

    @staticmethod
    async def create_emotion(user_id: str, emotion_code: str) -> None:
        emotion_service = EmotionService()
        await emotion_service.create_emotion(user_id=user_id, emotion_code=emotion_code)

    @staticmethod
    async def create_emotion_inventory() -> None:
        emotion_service = EmotionService()
        await emotion_service.create_emotion_inventory()

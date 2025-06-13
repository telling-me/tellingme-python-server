from app.services.emotion_service import EmotionService


class EmotionMother:

    @staticmethod
    async def create_emotion_inventory() -> None:
        emotion_service = EmotionService()
        await emotion_service.create_emotion_inventory()

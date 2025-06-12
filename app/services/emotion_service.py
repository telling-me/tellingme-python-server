from app.common.constants.emotion_dict import EMOTION_DICT
from app.dtos.emotion.emotion_data import EmotionData
from app.dtos.emotion.emotion_dto import EmotionDTO
from app.models.emotion import Emotion
from app.models.emotion_inventory import EmotionInventory
from app.models.user import User


class EmotionService:

    @classmethod
    async def create_emotion(cls, user_id: str, emotion_code: str) -> None:
        await Emotion.create_by_user_id(user_id=user_id, emotion_code=emotion_code)

    @classmethod
    async def create_emotion_inventory(cls) -> None:
        await EmotionInventory.create_bulk()

    @classmethod
    async def mapping_emotion_list(cls, user_id: str) -> EmotionDTO:
        user = await User.get_user_profile_by_user_id(user_id=user_id)

        if user.is_premium:
            emotions = await EmotionInventory.get_emotion_inventory()
        else:
            emotions = await Emotion.get_emotions_with_details_by_user_id(user_id=user_id)

        return EmotionDTO(emotionList=await cls.get_mapped_emotions(emotions))

    @classmethod
    async def get_mapped_emotions(cls, emotions: list[EmotionData]) -> list[int]:
        return [
            value for value in (EMOTION_DICT.get(emotion.emotion_code) for emotion in emotions) if value is not None
        ]

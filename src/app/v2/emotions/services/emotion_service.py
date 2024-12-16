from typing import Any

from app.v2.emotions.dtos.response import EmotionDTO, EmotionListResponseDTO
from app.v2.emotions.models.emotion import Emotion, EmotionInventory
from app.v2.users.services.user_service import UserService

emotion_mapping = {
    "EM_HAPPY": 1,
    "EM_PROUD": 2,
    "EM_OKAY": 3,
    "EM_TIRED": 4,
    "EM_SAD": 5,
    "EM_ANGRY": 6,
    "EM_EXCITED": 7,
    "EM_FUN": 8,
    "EM_RELAXED": 9,
    "EM_APATHETIC": 10,
    "EM_LONELY": 11,
    "EM_COMPLEX": 12,
}


class EmotionService:
    @classmethod
    async def get_emotions(cls, user_id: str) -> Any:
        return await Emotion.get_emotions_with_details_by_user_id(user_id=user_id)

    @classmethod
    async def add_emotion(cls, user_id: str, emotion_code: str) -> None:
        await Emotion.add_emotion(user_id=user_id, emotion_code=emotion_code)

    @classmethod
    async def get_emotion_inventory(cls) -> list[dict[str, str]]:
        return await EmotionInventory.get_emotion_inventory()

    @classmethod
    async def mapping_emotion_list(cls, user_id: str) -> EmotionDTO:
        user = await UserService.get_user_profile(user_id=user_id)

        if user.is_premium:
            emotions = await cls.get_emotion_inventory()
        else:
            emotions = await cls.get_emotions(user_id=user_id)

        return EmotionDTO.build(emotion_list=await cls.get_mapped_emotions(emotions))

    @classmethod
    async def get_mapped_emotions(cls, emotions: list[dict[str, str]]) -> list[int]:
        return [
            value
            for value in (emotion_mapping.get(emotion["emotion_code"]) for emotion in emotions)
            if value is not None
        ]

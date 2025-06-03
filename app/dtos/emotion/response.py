from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO


class EmotionDTO(BaseModel):
    emotionList: list[int]

    @classmethod
    def build(cls, emotion_list: list[int]) -> "EmotionDTO":
        return cls(emotionList=emotion_list)


class EmotionListResponseDTO(BaseResponseDTO):
    data: EmotionDTO

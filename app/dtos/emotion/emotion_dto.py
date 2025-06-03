from pydantic import BaseModel


class EmotionDTO(BaseModel):
    emotionList: list[int]

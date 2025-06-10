from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class EmotionDTO(BaseModel):
    model_config = FROZEN_CONFIG

    emotionList: list[int]

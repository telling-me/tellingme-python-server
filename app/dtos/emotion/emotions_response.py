from app.dtos.base_response import BaseResponseDTO
from app.dtos.emotion.emotion_dto import EmotionDTO
from app.dtos.frozen_config import FROZEN_CONFIG


class EmotionsResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: EmotionDTO

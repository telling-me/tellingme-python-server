from app.dtos.base_response import BaseResponseDTO
from app.dtos.emotion.emotion_dto import EmotionDTO


class EmotionsResponse(BaseResponseDTO):
    data: EmotionDTO

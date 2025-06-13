from fastapi import APIRouter, status

from app.dtos.emotion.emotions_response import EmotionsResponse
from app.services.emotion_service import EmotionService

emotion_router = APIRouter(prefix="/user/emotion", tags=["Emotion"])


@emotion_router.get(
    "",
    response_model=EmotionsResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_emotions(user_id: str) -> EmotionsResponse:
    return EmotionsResponse(
        data=await EmotionService.mapping_emotion_list(user_id=user_id),
        code=status.HTTP_200_OK,
        message="보유 감정 정보 조회",
    )

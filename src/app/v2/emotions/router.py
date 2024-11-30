from fastapi import APIRouter, status

from app.v2.emotions.dtos.response import EmotionListResponseDTO
from app.v2.emotions.services.emotion_service import EmotionService

router = APIRouter(prefix="/user/emotion", tags=["Emotion"])


@router.get(
    "",
    response_model=EmotionListResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_user_emotion_handler(user_id: str) -> EmotionListResponseDTO:
    return EmotionListResponseDTO(
        data=await EmotionService.mapping_emotion_list(user_id=user_id),
        code=status.HTTP_200_OK,
        message="보유 감정 정보 조회",
    )

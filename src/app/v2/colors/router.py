from fastapi import APIRouter, status

from app.v2.colors.dtos.response import ColorListResponseDTO
from app.v2.colors.services.color_service import ColorService

router = APIRouter(prefix="/user/color", tags=["Color"])


@router.get(
    "",
    response_model=ColorListResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_user_badge_handler(user_id: str):

    colors = await ColorService.get_colors_with_details_by_user_id(user_id=user_id)

    return ColorListResponseDTO(
        code=status.HTTP_200_OK,
        message="보유 색상 정보 조회",
        data=colors,
    )

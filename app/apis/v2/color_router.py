from fastapi import APIRouter, status

from app.dtos.color.colors_response import ColorsResponse
from app.services.color_service import ColorService

color_router = APIRouter(prefix="/user/color", tags=["Color"])


@color_router.get(
    "",
    response_model=ColorsResponse,
    status_code=status.HTTP_200_OK,
)
async def api_get_user_colors(user_id: str) -> ColorsResponse:
    return ColorsResponse(
        code=status.HTTP_200_OK,
        message="보유 색상 정보 조회",
        data=await ColorService.get_colors_with_details_by_user_id(user_id=user_id),
    )

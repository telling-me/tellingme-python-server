from fastapi import APIRouter, status

from app.dtos.badge.badges_response import BadgesResponse
from app.services.badge_service import BadgeService

badge_router = APIRouter(prefix="/user/badge", tags=["Badge"])


@badge_router.get(
    "",
    response_model=BadgesResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_badge_handler(user_id: str) -> BadgesResponse:
    badges = await BadgeService.get_badges_with_details_by_user_id(user_id)
    return BadgesResponse(
        code=status.HTTP_200_OK,
        message="보유 뱃지 정보 조회",
        data=badges,
    )

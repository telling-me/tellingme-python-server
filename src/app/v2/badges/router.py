from fastapi import APIRouter, status

from app.v2.badges.dtos.response import BadgeListResponseDTO
from app.v2.badges.services.badge_service import BadgeService

router = APIRouter(prefix="/user/badge", tags=["Badge"])


@router.get(
    "",
    response_model=BadgeListResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_user_badge_handler(user_id: str) -> BadgeListResponseDTO:

    badges = await BadgeService.get_badges_with_details_by_user_id(user_id)

    return BadgeListResponseDTO(
        code=status.HTTP_200_OK,
        message="보유 뱃지 정보 조회",
        data=badges,
    )

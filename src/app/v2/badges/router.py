from fastapi import APIRouter, status

from app.v2.badges.dtos.badge_dto import BadgeDTO, BadgeListDTO
from app.v2.badges.dtos.response import BadgeListResponseDTO
from app.v2.badges.models.badge import Badge

router = APIRouter(prefix="/user/badge", tags=["Badge"])


@router.get(
    "/",
    response_model=BadgeListResponseDTO,
    status_code=status.HTTP_200_OK,
)
async def get_user_badge_handler():
    uuid_bytes = b"\x18\nN@b\xf8F\xbe\xb1\xeb\xe7\xe3\xdd\x91\xcd\xdf"

    badge_list = await Badge.get_badges_with_details_by_user_id(uuid_bytes=uuid_bytes)

    badges = [
        BadgeDTO(
            badgeCode=item.get("badge_code"),
            badgeName=item.get("badge_name"),
            badgeMiddleName=item.get("badge_middle_name"),
            badgeCondition=item.get("badge_condition"),
        )
        for item in badge_list
    ]

    return BadgeListResponseDTO(
        code=status.HTTP_200_OK,
        message="보유 뱃지 정보 조회",
        data=BadgeListDTO(badges=badges),
    )

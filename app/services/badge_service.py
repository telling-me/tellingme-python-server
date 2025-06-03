from app.dtos.badge.badge_dto import BadgeDTO
from app.dtos.badge.badge_code_dto import BadgeCodeDTO
from app.models.badge import Badge, BadgeInventory


class BadgeService:
    @classmethod
    async def get_badges(cls, user_id: str) -> list[BadgeCodeDTO]:
        badges_raw = await Badge.get_badge_codes_by_user_id(user_id=user_id)
        return [BadgeCodeDTO.builder(badge) for badge in badges_raw]

    @classmethod
    async def get_badges_with_details_by_user_id(cls, user_id: str) -> list[BadgeDTO]:
        badges = await Badge.get_badges_with_details_by_user_id(user_id=user_id)
        return [
            BadgeDTO(
                badgeCode=badge.badge_code,
                badgeName=badge.badge_name,
                badgeCondition=badge.badge_condition,
                badgeMiddleName=badge.badge_middle_name,
            )
            for badge in badges
        ]

    @classmethod
    async def get_badge_count(cls, user_id: str) -> int:
        badge_count_raw = await Badge.get_badge_count_by_user_id(user_id=user_id)
        if badge_count_raw is None:
            return 0
        return int(badge_count_raw.get("badge_count", 0))

    @classmethod
    async def get_badge_info_by_badge_code(cls, badge_code: str) -> BadgeInventory:
        return await BadgeInventory.get(badge_code=badge_code)

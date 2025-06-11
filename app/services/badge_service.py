from app.dtos.badge.badge_dto import BadgeDTO
from app.models.badge import Badge


class BadgeService:

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
        return await Badge.get_badge_count_by_user_id(user_id=user_id)

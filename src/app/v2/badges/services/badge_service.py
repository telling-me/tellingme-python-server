from app.v2.badges.dtos.badge_dto import BadgeCodeDTO, BadgeDTO
from app.v2.badges.models.badge import Badge, BadgeInventory


class BadgeService:
    @classmethod
    async def get_badges(cls, user_id: str) -> list[BadgeCodeDTO]:
        badges_raw = await Badge.get_badge_codes_by_user_id(user_id=user_id)
        return [BadgeCodeDTO.builder(badge) for badge in badges_raw]

    @classmethod
    async def add_badge(cls, user_id: str, badge_code: str) -> None:
        await Badge.add_badge(user_id=user_id, badge_code=badge_code)

    @classmethod
    async def get_badges_with_details_by_user_id(cls, user_id: str) -> list[BadgeDTO]:
        badges_raw = await Badge.get_badges_with_details_by_user_id(user_id=user_id)
        return [BadgeDTO.builder(badge) for badge in badges_raw]

    @classmethod
    async def get_badge_count(cls, user_id: str) -> int:
        badge_count_raw = await Badge.get_badge_count_by_user_id(user_id=user_id)
        if badge_count_raw is None:
            return 0
        return int(badge_count_raw.get("badge_count", 0))

    @classmethod
    async def get_badge_info_by_badge_code(cls, badge_code: str) -> BadgeInventory:
        return await BadgeInventory.get(badge_code=badge_code)

from app.v2.badges.dtos.badge_dto import BadgeCodeDTO
from app.v2.badges.models.badge import Badge


class BadgeService:
    @classmethod
    async def get_badges(cls, user_id: str) -> list[BadgeCodeDTO]:
        badges_raw = await Badge.get_badge_codes_by_user_id(user_id=user_id)
        return [BadgeCodeDTO.builder(badge) for badge in badges_raw]

    @classmethod
    async def add_badge(cls, user_id: str, badge_code: str) -> None:
        await Badge.add_badge(user_id=user_id, badge_code=badge_code)

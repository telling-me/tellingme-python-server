from app.services.badge_service import BadgeService


class BadgeMother:

    @staticmethod
    async def create_badge(user_id: str, badge_code: str) -> None:
        badge_service = BadgeService()
        await badge_service.create_badge(user_id=user_id, badge_code=badge_code)

    @staticmethod
    async def create_badge_inventory() -> None:
        badge_service = BadgeService()
        await badge_service.create_badge_inventory()

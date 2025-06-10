from typing import Optional

from app.dtos.teller_card.teller_card_dto import TellerCardDTO
from app.models.badge import BadgeInventory
from app.models.color_inventory import ColorInventory
from app.models.teller_card import TellerCard


class TellerCardService:
    @classmethod
    async def get_teller_card(cls, user_id: str) -> TellerCardDTO:
        teller_card = await TellerCard.get_teller_card_info_by_user_id(user_id=user_id)
        return TellerCardDTO(
            badgeCode=teller_card.activate_badge_code,
            badgeName=teller_card.badge_name,
            badgeMiddleName=teller_card.badge_middle_name,
            colorCode=teller_card.activate_color_code,
        )

    @classmethod
    async def patch_teller_card(
        cls, user_id: str, badge_code: str | None = None, color_code: str | None = None
    ) -> TellerCardDTO:
        await cls._validate_teller_card(badge_code=badge_code, color_code=color_code)

        await TellerCard.patch_teller_card_info_by_user_id(
            user_id=user_id, badge_code=badge_code, color_code=color_code
        )

        return await cls.get_teller_card(user_id=user_id)

    @classmethod
    async def _validate_teller_card(cls, badge_code: str | None, color_code: str | None) -> None:
        badge_code_list = await BadgeInventory.all().values("badge_code")
        color_code_list = await ColorInventory.all().values("color_code")
        badge_codes = [badge["badge_code"] for badge in badge_code_list]
        color_codes = [color["color_code"] for color in color_code_list]

        if badge_code and badge_code not in badge_codes:
            raise ValueError("Invalid badge code")

        if color_code and color_code not in color_codes:
            raise ValueError("Invalid color code")

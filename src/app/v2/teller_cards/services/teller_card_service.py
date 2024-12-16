from typing import Optional

from app.v2.badges.models.badge import BadgeInventory
from app.v2.colors.models.color import ColorInventory
from app.v2.teller_cards.dtos.teller_card_dto import TellerCardDTO
from app.v2.teller_cards.models.teller_card import TellerCard


class TellerCardService:
    @classmethod
    async def get_teller_card(cls, user_id: str) -> TellerCardDTO:
        teller_cards_raw: dict[str, str] = await TellerCard.get_teller_card_info_by_user_id(user_id=user_id)
        return TellerCardDTO.builder(teller_cards_raw)

    @classmethod
    async def patch_teller_card(
        cls, user_id: str, badge_code: Optional[str] = None, color_code: Optional[str] = None
    ) -> None:
        await TellerCard.patch_teller_card_info_by_user_id(
            user_id=user_id, badge_code=badge_code, color_code=color_code
        )

    @classmethod
    async def validate_teller_card(cls, badge_code: Optional[str], color_code: Optional[str]) -> None:
        badge_code_list = await BadgeInventory.all().values("badge_code")
        color_code_list = await ColorInventory.all().values("color_code")
        badge_codes = [badge["badge_code"] for badge in badge_code_list]
        color_codes = [color["color_code"] for color in color_code_list]

        if badge_code and badge_code not in badge_codes:
            raise ValueError("Invalid badge code")

        if color_code and color_code not in color_codes:
            raise ValueError("Invalid color code")

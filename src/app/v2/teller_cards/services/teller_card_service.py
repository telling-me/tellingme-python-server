from app.v2.teller_cards.dtos.teller_card_dto import TellerCardDTO
from app.v2.teller_cards.models.teller_card import TellerCard


class TellerCardService:
    @classmethod
    async def get_teller_card(cls, user_id: str) -> TellerCardDTO:
        teller_cards_raw = await TellerCard.get_teller_card_info_by_user_id(
            user_id=user_id
        )
        return TellerCardDTO.builder(teller_cards_raw)

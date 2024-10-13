from pydantic import BaseModel

from app.v2.teller_cards.dtos.teller_card_dto import TellerCardDTO


class UserInfoDTO(BaseModel):
    nickname: str
    cheeseBalance: int
    tellerCard: TellerCardDTO

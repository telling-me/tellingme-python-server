from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG
from app.dtos.teller_card.teller_card_dto import TellerCardDTO


class UserInfoDTO(BaseModel):
    model_config = FROZEN_CONFIG

    nickname: str
    cheeseBalance: int
    tellerCard: TellerCardDTO

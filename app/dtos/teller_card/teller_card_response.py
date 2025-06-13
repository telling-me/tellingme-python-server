from app.dtos.base_response import BaseResponseDTO
from app.dtos.frozen_config import FROZEN_CONFIG
from app.dtos.teller_card.teller_card_dto import TellerCardDTO


class TellerCardResponse(BaseResponseDTO):
    model_config = FROZEN_CONFIG

    data: TellerCardDTO

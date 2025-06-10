from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO
from app.dtos.teller_card.teller_card_dto import TellerCardDTO


class TellerCardResponse(BaseResponseDTO):
    data: TellerCardDTO

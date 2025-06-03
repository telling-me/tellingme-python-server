from pydantic import BaseModel

from app.dtos.base_response import BaseResponseDTO
from app.dtos.teller_card.teller_card_dto import TellerCardDTO as TellerCardLogicDTO


class TellerCardDTO(BaseModel):
    colorCode: str
    badgeCode: str


class TellerCardResponseDTO(BaseResponseDTO):
    data: TellerCardDTO

    @classmethod
    def builder(cls, teller_card: TellerCardLogicDTO) -> "TellerCardResponseDTO":
        return cls(
            code=200,
            message="success",
            data=TellerCardDTO(colorCode=teller_card.colorCode, badgeCode=teller_card.badgeCode),
        )

from pydantic import BaseModel

from common.base_models.base_dtos.base_response import BaseResponseDTO


class TellerCardDTO(BaseModel):
    colorCode: str
    badgeCode: str


class TellerCardResponseDTO(BaseResponseDTO):
    data: TellerCardDTO

    @classmethod
    def builder(cls, teller_card: TellerCardDTO) -> "TellerCardResponseDTO":
        return cls(
            code=200,
            message="success",
            data=TellerCardDTO(
                colorCode=teller_card.colorCode, badgeCode=teller_card.badgeCode
            ),
        )

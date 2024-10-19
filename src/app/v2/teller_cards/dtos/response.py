from pydantic import BaseModel


class TellerCardResponseDTO(BaseModel):
    colorCode: str
    badgeCode: str

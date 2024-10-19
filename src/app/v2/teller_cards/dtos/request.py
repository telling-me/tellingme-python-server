from pydantic import BaseModel


class TellerCardRequestDTO(BaseModel):
    colorCode: str
    badgeCode: str

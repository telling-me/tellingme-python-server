from pydantic import BaseModel


class TellerCardRequestDTO(BaseModel):
    user_id: str
    colorCode: str
    badgeCode: str

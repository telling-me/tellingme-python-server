from pydantic import BaseModel


class TellerCardDTO(BaseModel):
    badgeCode: str
    badgeName: str
    badgeMiddleName: str
    colorCode: str

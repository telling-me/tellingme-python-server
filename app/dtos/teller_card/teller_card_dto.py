from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class TellerCardDTO(BaseModel):
    model_config = FROZEN_CONFIG

    colorCode: str
    badgeCode: str
    badgeName: str
    badgeMiddleName: str

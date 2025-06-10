from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class UserProfileDTO(BaseModel):
    model_config = FROZEN_CONFIG

    nickname: str
    badgeCode: str
    cheeseBalance: int
    badgeCount: int
    answerCount: int
    premium: bool
    allowNotification: bool

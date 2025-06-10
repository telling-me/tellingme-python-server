from typing import Optional

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class TellerCardRequest(BaseModel):
    model_config = FROZEN_CONFIG

    user_id: str
    colorCode: str | None = None
    badgeCode: str | None = None

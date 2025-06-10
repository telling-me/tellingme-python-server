from __future__ import annotations

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class BadgeDTO(BaseModel):
    model_config = FROZEN_CONFIG

    badgeCode: str
    badgeName: str
    badgeMiddleName: str
    badgeCondition: str

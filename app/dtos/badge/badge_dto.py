from __future__ import annotations

from pydantic import BaseModel


class BadgeDTO(BaseModel):
    badgeCode: str
    badgeName: str
    badgeMiddleName: str
    badgeCondition: str

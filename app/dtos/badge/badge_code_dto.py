from __future__ import annotations

from pydantic import BaseModel


class BadgeCodeDTO(BaseModel):
    badgeCode: str

    @classmethod
    def builder(cls, badge_raw: dict[str, str]) -> BadgeCodeDTO:
        return cls(badgeCode=badge_raw.get("badge_code", ""))

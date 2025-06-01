from pydantic import BaseModel


class BadgeCodeDTO(BaseModel):
    badgeCode: str

    @classmethod
    def builder(cls, badge_raw: dict[str, str]) -> "BadgeCodeDTO":
        return cls(badgeCode=badge_raw.get("badge_code", ""))


class BadgeDTO(BaseModel):
    badgeCode: str
    badgeName: str
    badgeMiddleName: str
    badgeCondition: str

    @classmethod
    def builder(cls, badge_raw: dict[str, str]) -> "BadgeDTO":
        return cls(
            badgeCode=badge_raw.get("badge_code", ""),
            badgeName=badge_raw.get("badge_name", ""),
            badgeMiddleName=badge_raw.get("badge_middle_name", ""),
            badgeCondition=badge_raw.get("badge_condition", ""),
        )

from pydantic import BaseModel


class BadgeCodeDTO(BaseModel):
    badgeCode: str

    @classmethod
    def builder(cls, badge_raw: dict) -> "BadgeCodeDTO":
        return cls(badgeCode=badge_raw.get("badge_code"))


class BadgeDTO(BaseModel):
    badgeCode: str
    badgeName: str
    badgeMiddleName: str
    badgeCondition: str


class BadgeListDTO(BaseModel):
    badges: list[BadgeDTO]

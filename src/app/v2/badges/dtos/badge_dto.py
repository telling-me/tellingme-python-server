from pydantic import BaseModel


class BadgeCodeDTO(BaseModel):
    badgeCode: str


class BadgeDTO(BaseModel):
    badgeCode: str
    badgeName: str
    badgeMiddleName: str
    badgeCondition: str


class BadgeListDTO(BaseModel):
    badges: list[BadgeDTO]

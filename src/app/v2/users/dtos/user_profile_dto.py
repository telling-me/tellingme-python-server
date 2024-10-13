from pydantic import BaseModel


class UserProfileDto(BaseModel):
    nickname: str
    badgeCode: str
    cheeseBalance: int
    badgeCount: int
    answerCount: int
    premium: bool

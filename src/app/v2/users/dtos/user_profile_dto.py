from pydantic import BaseModel


class UserProfileDTO(BaseModel):
    nickname: str
    badgeCode: str
    cheeseBalance: int
    badgeCount: int
    answerCount: int
    premium: bool

from pydantic import BaseModel


class UserProfileDTO(BaseModel):
    nickname: str
    badgeCode: str
    cheeseBalance: int
    badgeCount: int
    answerCount: int
    premium: bool

    @classmethod
    def builder(
        cls,
        nickname: str,
        badgeCode: str,
        cheeseBalance: int,
        badgeCount: int,
        answerCount: int,
        premium: bool,
    ) -> "UserProfileDTO":
        return cls(
            nickname=nickname,
            badgeCode=badgeCode,
            cheeseBalance=cheeseBalance,
            badgeCount=badgeCount,
            answerCount=answerCount,
            premium=premium,
        )

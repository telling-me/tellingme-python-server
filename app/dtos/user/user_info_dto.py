from pydantic import BaseModel

from app.dtos.teller_card.teller_card_dto import TellerCardDTO


class UserInfoDTO(BaseModel):
    nickname: str
    cheeseBalance: int
    tellerCard: TellerCardDTO

    @classmethod
    def builder(cls, user_raw: dict[str, str], cheeseBalance: int, tellerCard: TellerCardDTO) -> "UserInfoDTO":
        return cls(
            nickname=user_raw.get("nickname", ""),
            cheeseBalance=cheeseBalance,
            tellerCard=tellerCard,
        )

from pydantic import BaseModel


class TellerCardDTO(BaseModel):
    badgeCode: str
    badgeName: str
    badgeMiddleName: str
    colorCode: str

    @classmethod
    def builder(cls, teller_card_raw: dict) -> "TellerCardDTO":
        return cls(
            badgeCode=teller_card_raw.get("activate_badge_code"),
            badgeName=teller_card_raw.get("badge_name"),
            badgeMiddleName=teller_card_raw.get("badge_middle_name"),
            colorCode=teller_card_raw.get("activate_color_code"),
        )

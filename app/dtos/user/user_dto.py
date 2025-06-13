import dataclasses


@dataclasses.dataclass(frozen=True)
class UserProfileData:
    user_id: str
    nickname: str
    profile_url: str
    is_premium: bool
    user_status: bool
    cheese_manager_id: int
    teller_card_id: int
    level_id: int
    allow_notification: bool

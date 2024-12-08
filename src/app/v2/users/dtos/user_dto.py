from typing import Any, Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    user_id: Optional[str] = None
    nickname: Optional[str] = None
    profile_url: Optional[str] = None
    is_premium: Optional[bool] = None
    user_status: Optional[bool] = None
    cheese_manager_id: Optional[int] = None
    teller_card_id: Optional[int] = None
    level_id: Optional[int] = None
    allow_notification: Optional[bool] = None

    @classmethod
    def build(cls, user: dict[str, Any]) -> "UserDTO":
        is_premium = user.get("is_premium") != b"\x00"
        allow_notification = user.get("allow_notification") != b"\x00"
        return cls(
            user_id=user.get("user_id", None),
            nickname=user.get("nickname", None),
            profile_url=user.get("profile_url", None),
            is_premium=is_premium,
            user_status=user.get("user_status", None),
            cheese_manager_id=user.get("cheese_manager_id", None),
            teller_card_id=user.get("teller_card_id", None),
            level_id=user.get("level_id", None),
            allow_notification=allow_notification,
        )

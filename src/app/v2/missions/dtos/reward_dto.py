from typing import Any, Optional

from pydantic import BaseModel


class RewardDTO(BaseModel):
    total_cheese: int
    total_exp: int
    badge_code: Optional[str] = None
    badge_full_name: Optional[str] = None

    class META:
        orm_mode = True

    @classmethod
    async def build(
        cls,
        total_cheese: int,
        total_exp: int,
        badge_code: Optional[str] = None,
        badge_full_name: Optional[str] = None,
    ) -> "RewardDTO":
        return cls(
            total_cheese=total_cheese,
            total_exp=total_exp,
            badge_code=badge_code,
            badge_full_name=badge_full_name,
        )

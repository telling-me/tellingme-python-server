from typing import Any, Optional

from pydantic import BaseModel


class RewardDTO(BaseModel):
    total_cheese: int
    total_exp: int
    badge: Optional[str] = None

    @classmethod
    async def build(cls, total_cheese: int, total_exp: int, badge: Optional[str] = None) -> "RewardDTO":
        return cls(
            total_cheese=total_cheese,
            total_exp=total_exp,
            badge=badge,
        )

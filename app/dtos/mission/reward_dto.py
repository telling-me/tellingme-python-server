from typing import Optional

from pydantic import BaseModel, ConfigDict


class RewardDTO(BaseModel):
    total_cheese: int
    total_exp: int
    badge_code: Optional[str] = None
    badge_full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

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

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class RewardDTO(BaseModel):
    model_config = FROZEN_CONFIG

    total_cheese: int
    total_exp: int
    badge_code: str | None = None
    badge_full_name: str | None = None

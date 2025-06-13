from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class LevelDTO(BaseModel):
    model_config = FROZEN_CONFIG

    level: int
    currentExp: int
    requiredExp: int

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG
from app.dtos.level.level_dto import LevelDTO


class LevelInfoDTO(BaseModel):
    model_config = FROZEN_CONFIG

    levelDto: LevelDTO
    daysToLevelUp: int

from pydantic import BaseModel

from app.dtos.frozen_config import FROZEN_CONFIG


class ColorDTO(BaseModel):
    model_config = FROZEN_CONFIG

    colorCode: str
    colorName: str
    colorHexCode: str

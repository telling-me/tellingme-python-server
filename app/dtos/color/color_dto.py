from pydantic import BaseModel


class ColorDTO(BaseModel):
    colorCode: str
    colorName: str
    colorHexCode: str

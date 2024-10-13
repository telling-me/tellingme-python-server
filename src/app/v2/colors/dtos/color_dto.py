from pydantic import BaseModel


class ColorCodeDTO(BaseModel):
    colorCode: str

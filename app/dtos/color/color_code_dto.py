from pydantic import BaseModel


class ColorCodeDTO(BaseModel):
    colorCode: str

    @classmethod
    def builder(cls, color_raw: dict[str, str]) -> "ColorCodeDTO":
        return cls(colorCode=color_raw.get("color_code", ""))

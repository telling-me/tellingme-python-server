from pydantic import BaseModel


class ColorCodeDTO(BaseModel):
    colorCode: str

    @classmethod
    def builder(cls, color_raw: dict[str, str]) -> "ColorCodeDTO":
        return cls(colorCode=color_raw.get("color_code", ""))


class ColorDTO(BaseModel):
    colorCode: str
    # colorName: str
    # colorHexCode: str

    @classmethod
    def builder(cls, color_raw: dict[str, str]) -> "ColorDTO":
        return cls(
            colorCode=color_raw.get("color_code", ""),
            # colorName=color_raw.get("color_name", ""),
            # colorHexCode=color_raw.get("color_hex_code", ""),
        )

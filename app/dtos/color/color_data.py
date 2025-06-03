import dataclasses


@dataclasses.dataclass(frozen=True)
class ColorData:
    color_code: str
    color_name: str
    color_hex_code: str

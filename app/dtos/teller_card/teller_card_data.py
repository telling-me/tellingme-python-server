import dataclasses


@dataclasses.dataclass(frozen=True)
class TellerCardData:
    activate_color_code: str
    activate_badge_code: str
    badge_name: str
    badge_middle_name: str

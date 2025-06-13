import dataclasses


@dataclasses.dataclass(frozen=True)
class BadgeData:
    badge_code: str
    badge_name: str
    badge_condition: str
    badge_middle_name: str

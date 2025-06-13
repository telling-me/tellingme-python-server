import dataclasses


@dataclasses.dataclass(frozen=True)
class LevelData:
    level_exp: int
    level_level: int
    required_exp: int

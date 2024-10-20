from pydantic import BaseModel


class LevelDTO(BaseModel):
    level: int
    current_exp: int

    @classmethod
    def builder(cls, level: int, current_exp: int) -> "LevelDTO":
        return cls(level=level, current_exp=current_exp)

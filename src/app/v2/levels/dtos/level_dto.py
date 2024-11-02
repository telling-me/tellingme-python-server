from pydantic import BaseModel


class LevelDTO(BaseModel):
    level: int
    current_exp: int
    required_exp: int | None = None

    @classmethod
    def builder(
        cls, level: int, current_exp: int, required_exp: int | None = None
    ) -> "LevelDTO":
        return cls(level=level, current_exp=current_exp, required_exp=required_exp)

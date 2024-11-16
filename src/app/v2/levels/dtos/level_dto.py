from pydantic import BaseModel


class LevelDTO(BaseModel):
    level: int
    current_exp: int
    required_exp: int | None = None

    @classmethod
    def builder(cls, level: dict) -> "LevelDTO":
        return cls(
            level=level["level_level"],
            current_exp=level["level_exp"],
            required_exp=level["required_exp"],
        )


class LevelInfoDTO(BaseModel):
    level_dto: LevelDTO
    days_to_level_up: int

    @classmethod
    def builder(cls, level_dto: LevelDTO, days_to_level_up: int) -> "LevelInfoDTO":
        return cls(
            level_dto=level_dto,
            days_to_level_up=days_to_level_up,
        )

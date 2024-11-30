from pydantic import BaseModel


class LevelDTO(BaseModel):
    level: int
    currentExp: int
    requiredExp: int | None = None

    @classmethod
    def builder(cls, level: dict) -> "LevelDTO":
        return cls(
            level=level["level_level"],
            currentExp=level["level_exp"],
            requiredExp=level["required_exp"],
        )


class LevelInfoDTO(BaseModel):
    levelDto: LevelDTO
    daysToLevelUp: int

    @classmethod
    def builder(cls, level_dto: LevelDTO, days_to_level_up: int) -> "LevelInfoDTO":
        return cls(
            levelDto=level_dto,
            daysToLevelUp=days_to_level_up,
        )

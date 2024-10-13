from pydantic import BaseModel


class LevelDto(BaseModel):
    level: int
    current_exp: int

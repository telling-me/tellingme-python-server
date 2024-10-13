from pydantic import BaseModel


class LevelDTO(BaseModel):
    level: int
    current_exp: int

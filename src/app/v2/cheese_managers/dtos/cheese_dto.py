from pydantic import BaseModel


class CheeseResponseDTO(BaseModel):
    cheeseBalance: int

    @classmethod
    def builder(cls, cheese_balance: int) -> "CheeseResponseDTO":
        return cls(cheeseBalance=cheese_balance)

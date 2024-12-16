from typing import Optional

from pydantic import BaseModel


class TellerCardRequestDTO(BaseModel):
    user_id: str
    colorCode: Optional[str] = None
    badgeCode: Optional[str] = None

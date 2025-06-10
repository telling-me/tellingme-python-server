import dataclasses
from datetime import date, datetime


@dataclasses.dataclass(frozen=True)
class AnswerData:
    answer_id: int
    content: str
    created_time: datetime
    date: date
    emotion: int
    is_premium: bool
    is_public: bool
    modified_time: datetime
    user_id: bytes
    is_blind: bool
    like_count: int
    is_spare: bool
    blind_ended_at: datetime | None = None
    blind_started_at: datetime | None = None

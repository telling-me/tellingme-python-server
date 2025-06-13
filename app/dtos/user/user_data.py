import dataclasses


@dataclasses.dataclass(frozen=True)
class UserData:
    nickname: str
    cheese_manager_id: int

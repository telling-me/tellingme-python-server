import dataclasses


@dataclasses.dataclass(frozen=True)
class MissionData:
    user_mission_id: int
    is_completed: bool
    mission_code: str
    progress_count: int

    @staticmethod
    def to_bool(val: str) -> bool:
        if isinstance(val, bytes):
            return bool(int.from_bytes(val, byteorder="big"))
        return bool(val)

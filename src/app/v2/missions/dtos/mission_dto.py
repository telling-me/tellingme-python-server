from typing import Any

from pydantic import BaseModel


class UserMissionDTO(BaseModel):
    user_mission_id: int
    is_completed: bool
    mission_code: str
    progress_count: int

    @classmethod
    def builder(cls, user_mission: dict[str, Any]) -> "UserMissionDTO":
        is_completed_raw = user_mission.get("is_completed")
        is_completed = (
            bool(int.from_bytes(is_completed_raw, byteorder="big"))
            if isinstance(is_completed_raw, bytes) and is_completed_raw is not None
            else bool(is_completed_raw) if is_completed_raw is not None else False
        )
        return cls(
            user_mission_id=user_mission.get("user_mission_id", 0),  # 기본값 0 설정
            is_completed=is_completed,
            mission_code=user_mission.get("mission_code", ""),  # 기본값 빈 문자열 설정
            progress_count=user_mission.get("progress_count", 0),  # 기본값 0 설정
        )

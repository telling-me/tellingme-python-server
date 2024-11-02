from pydantic import BaseModel


class UserMissionDTO(BaseModel):
    user_mission_id: int
    is_completed: bool
    mission_code: str
    progress_count: int

    @classmethod
    def builder(cls, user_mission) -> "UserMissionDTO":
        is_completed_raw = user_mission.get("is_completed")
        is_completed = (
            bool(int.from_bytes(is_completed_raw, byteorder="big"))
            if isinstance(is_completed_raw, bytes)
            else bool(is_completed_raw)
        )
        return cls(
            user_mission_id=user_mission.get("user_mission_id"),
            is_completed=is_completed,
            mission_code=user_mission.get("mission_code"),
            progress_count=user_mission.get("progress_count"),
        )

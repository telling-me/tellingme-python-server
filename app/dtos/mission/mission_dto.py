from pydantic import BaseModel


class UserMissionDTO(BaseModel):

    user_mission_id: int
    is_completed: bool
    mission_code: str
    progress_count: int

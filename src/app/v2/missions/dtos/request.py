from pydantic import BaseModel


class MissionProgressRequest(BaseModel):
    mission_code: str
    progress_count: int

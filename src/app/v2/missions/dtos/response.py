# 응답 모델 정의
from pydantic import BaseModel


class MissionProgressResponse(BaseModel):
    mission_code: str
    progress_count: int
    is_completed: bool
    mission_name: str
    mission_description: str
    target_count: int


class UserLevelResponse(BaseModel):
    user_level: int
    user_exp: int
    level_up: bool


class ApiResponse(BaseModel):
    mission_progress: MissionProgressResponse
    user_level_info: UserLevelResponse

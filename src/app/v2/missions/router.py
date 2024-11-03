from fastapi import APIRouter, HTTPException, Depends

from tortoise.expressions import F

from app.v2.items.models.item import RewardInventory
from app.v2.likes.models.like import Like
from app.v2.missions.dtos.request import MissionProgressRequest
from app.v2.missions.dtos.response import (
    ApiResponse,
    MissionProgressResponse,
    UserLevelResponse,
)
from app.v2.missions.models.mission import MissionInventory, UserMission
from app.v2.missions.services.mission_service import MissionService
from app.v2.users.models.user import User
from common.utils.get_user_id import get_user_id

router = APIRouter(prefix="/mission", tags=["Mission"])


@router.post("/level")
def level_up_handler():
    pass


@router.post("/update-mission-progress", response_model=ApiResponse)
async def update_mission_progress(
    request: MissionProgressRequest, user_id: str = Depends(get_user_id)
):
    user: User = await User.get_user_by_uuid(user_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # 미션 정보를 가져옵니다.
    mission = await MissionInventory.get_or_none(mission_code=request.mission_code)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    user_mission, created = await UserMission.get_or_create(
        user=user,
        mission_code=request.mission_code,
        defaults={"progress_count": 0, "is_completed": False},
    )

    level_up = False
    if not user_mission.is_completed:
        # 미션 진행 상황을 업데이트합니다.
        user_mission.progress_count = F("progress_count") + request.progress_count
        await user_mission.save()
        await user_mission.refresh_from_db()

        # 미션 완료 여부를 확인합니다.
        if user_mission.progress_count >= mission.target_count:
            user_mission.is_completed = True
            await user_mission.save()

            # 레벨업 미션인 경우 처리
            if mission.condition_type == "LEVEL_UP":
                user.level.user_level += 1
                await user.level.save()
                level_up = True
                # 여기에 레벨업 보상 로직을 추가할 수 있습니다.

    return ApiResponse(
        mission_progress=MissionProgressResponse(
            mission_code=mission.mission_code,
            progress_count=user_mission.progress_count,
            is_completed=user_mission.is_completed,
            mission_name=mission.mission_name,
            mission_description=mission.mission_description,
            target_count=mission.target_count,
        ),
        user_level_info=UserLevelResponse(
            user_level=user.level.user_level, level_up=level_up
        ),
    )


@router.get("/get-user-missions")
async def mission_test_handler(user_id: str = Depends(get_user_id)):

    mission_service = MissionService()

    await mission_service.update_mission_progress(user_id=user_id)

    await mission_service.validate_reward(reward_code="RW_FIRST_POST")

    # 3. 특정 시간대 미션도 체크하여 진행
    # if "time_check" in action_data:
    #     await update_mission_progress(user_id, action_data["time_check"], increment=1)
    # pass

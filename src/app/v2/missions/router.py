from fastapi import APIRouter, Depends

from app.v2.missions.services.mission_service import MissionService
from common.utils.get_user_id import get_user_id

router = APIRouter(prefix="/mission", tags=["Mission"])


@router.get("/get-user-missions")
async def mission_test_handler(user_id: str = Depends(get_user_id)):

    mission_service = MissionService()

    await mission_service.update_mission_progress(user_id=user_id)

    # await mission_service.validate_reward(reward_code="RW_FIRST_POST")

    # 3. 특정 시간대 미션도 체크하여 진행
    # if "time_check" in action_data:
    #     await update_mission_progress(user_id, action_data["time_check"], increment=1)
    # pass

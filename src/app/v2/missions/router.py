from fastapi import APIRouter, BackgroundTasks

from app.v2.missions.services.mission_service import MissionService

router = APIRouter(prefix="/mission", tags=["Mission"])


async def process_mission_in_background(user_id: str):
    mission_service = MissionService()
    await mission_service.update_mission_progress(user_id)


@router.get("")
async def mission_handler(user_id: str, background_tasks: BackgroundTasks) -> None:
    background_tasks.add_task(process_mission_in_background, user_id)

    # await mission_service.validate_reward(reward_code="RW_FIRST_POST")

    # 3. 특정 시간대 미션도 체크하여 진행
    # if "time_check" in action_data:
    #     await update_mission_progress(user_id, action_data["time_check"], increment=1)
    # pass

from app.v2.missions.models.mission import UserMission


async def mission_reset_task() -> None:
    await UserMission.filter(mission_code__in=["MS_LV_UP", "MS_DAILY_LIKE_3_PER_DAY", "MS_SINGLE_POST_2_5"]).update(
        is_completed=False
    )

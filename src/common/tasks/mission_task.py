import asyncio

from app.v2.missions.models.mission import UserMission


async def mission_reset_task() -> None:
    await asyncio.gather(
        UserMission.filter(mission_code__in=["MS_LV_UP", "MS_DAILY_LIKE_3_PER_DAY", "MS_DAILY_POST_GENERAL"]).update(
            is_completed=False, progress_count=0
        ),
    )

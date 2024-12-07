import asyncio

from tortoise.expressions import Q

from app.v2.missions.models.mission import UserMission


async def mission_reset_task() -> None:
    await asyncio.gather(
        UserMission.filter(Q(mission_code="MS_SINGLE_POST_2_5", progress_count__lt=3)).update(is_completed=False),
        UserMission.filter(mission_code__in=["MS_LV_UP", "MS_DAILY_LIKE_3_PER_DAY"]).update(is_completed=False),
    )

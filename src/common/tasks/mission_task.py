import asyncio

from tortoise.expressions import Q

from app.v2.missions.models.mission import UserMission


async def mission_reset_task() -> None:
    await asyncio.gather(
        UserMission.filter(Q(mission_code="MS_SINGLE_POST_2_5", progress_count__lt=3)).update(is_completed=False),
        UserMission.filter(mission_code__in=["MS_LV_UP", "MS_DAILY_LIKE_3_PER_DAY", "MS_DAILY_POST_GENERAL"]).update(
            is_completed=False, progress_count=0
        ),
    )
    # 좋아요, 일반은 progress count도 수정

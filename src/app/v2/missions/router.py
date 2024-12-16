from fastapi import APIRouter

from core.configs.celery_settings import process_mission_in_background

router = APIRouter(prefix="/mission", tags=["Mission"])


@router.get("")
async def mission_handler(user_id: str) -> None:
    process_mission_in_background.delay(user_id)

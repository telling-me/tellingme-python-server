from typing import Any

from fastapi import APIRouter, Depends

from app.v2.missions.services.mission_service import MissionService
from core.configs.celery_settings import process_mission_in_background

router = APIRouter(prefix="/mission", tags=["Mission"])


@router.get("")
async def mission_handler(user_id: str) -> None:
    process_mission_in_background.delay(user_id)


@router.get("/direct")
async def mission_handler_direct(
    user_id: str,
    mission_service: MissionService = Depends(),
) -> dict[str, Any]:
    await mission_service.update_mission_progress(user_id=user_id)
    return {
        "code": 200,
        "message": "success",
        "data": True,
    }

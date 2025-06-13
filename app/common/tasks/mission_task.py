from app.services.mission_service import MissionService


async def mission_reset_task() -> None:
    mission_service = MissionService()
    await mission_service.reset_mission()

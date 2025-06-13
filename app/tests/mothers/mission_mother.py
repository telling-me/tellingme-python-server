from app.services.mission_service import MissionService


class MissionMother:

    @staticmethod
    async def create_mission_inventory() -> None:
        mission_service = MissionService()
        await mission_service.create_mission_inventory()

    @staticmethod
    async def reset_mission() -> None:
        mission_service = MissionService()
        await mission_service.reset_mission()

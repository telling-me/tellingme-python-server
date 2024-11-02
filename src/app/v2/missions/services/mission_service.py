import asyncio

from app.v2.missions.dtos.mission_dto import UserMissionDTO
from app.v2.missions.models.mission import UserMission, MissionInventory


class MissionService:
    @staticmethod
    async def get_user_missions(user_id, condition_type):
        user_mission_raw = await UserMission.get_user_missions_by_condition_type(
            user_id, condition_type
        )
        return [
            UserMissionDTO.builder(user_mission) for user_mission in user_mission_raw
        ]

    @staticmethod
    async def update_user_mission_progress(
        user_id: str,
        mission_code: str,
        new_progress_count: int,
        is_completed: bool,
    ):
        await UserMission.update_user_mission_progress(
            user_id=user_id,
            mission_code=mission_code,
            new_progress_count=new_progress_count,
            is_completed=is_completed,
        )

    async def update_mission_progress(self, user_id, condition_type, increment=1):
        # 1. 해당 조건 유형의 미션을 조회하고 진행 상황 업데이트
        user_missions = await self.get_user_missions(user_id, condition_type)
        missions = await MissionInventory.filter(condition_type=condition_type).all()

        mission_dict = {mission.mission_code: mission for mission in missions}

        for user_mission in user_missions:
            if user_mission.is_completed:
                continue

            # 2. 진행 상황 증가
            user_mission.progress_count += increment

            mission = mission_dict.get(user_mission.mission_code)
            if not mission:
                continue

            # 3. 목표 도달 여부 확인
            if user_mission.progress_count >= mission.target_count:
                user_mission.is_completed = True  # 미션 완료 처리
                # await self.reward_user_for_mission(
                #     user_id, user_mission.mission.reward_code
                # )  # 보상 지급

            await self.update_user_mission_progress(
                user_id=user_id,
                mission_code=user_mission.mission_code,
                new_progress_count=user_mission.progress_count,
                is_completed=user_mission.is_completed,
            )

    @staticmethod
    async def reward_user_for_mission(user_id, reward_code):
        print(f"Reward {reward_code} granted to user {user_id}")

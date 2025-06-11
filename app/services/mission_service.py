import asyncio
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from app.common.constants.item_category import ItemCategory
from app.common.constants.mission_condition import MS
from app.common.constants.reward_type import RewardType
from app.core.configs import settings
from app.dtos.mission.mission_dto import UserMissionDTO
from app.dtos.mission.reward_dto import RewardDTO
from app.models.answer import Answer
from app.models.badge import Badge
from app.models.badge_inventory import BadgeInventory
from app.models.cheese_manager import CheeseManager
from app.models.color import Color
from app.models.item import ItemInventory, ItemInventoryRewardInventory, RewardInventory
from app.models.like import Like
from app.models.mission import UserMission
from app.models.mission_inventory import MissionInventory
from app.models.user import User
from app.services.answer_service import AnswerService
from app.services.level_service import LevelService
from app.services.notice_service import NoticeService


class MissionService:
    @staticmethod
    async def get_user_missions(user_id: str) -> list[UserMissionDTO]:
        user_missions = await UserMission.get_user_missions_by_condition_type(user_id)
        return [
            UserMissionDTO(
                user_mission_id=user_mission.user_mission_id,
                is_completed=user_mission.is_completed,
                mission_code=user_mission.mission_code,
                progress_count=user_mission.progress_count,
            )
            for user_mission in user_missions
        ]

    @staticmethod
    async def _update_user_mission_progress(
        user_id: str,
        mission_code: str,
        new_progress_count: int,
        is_completed: bool,
    ) -> None:
        await UserMission.update_user_mission_progress(
            user_id=user_id,
            mission_code=mission_code,
            new_progress_count=new_progress_count,
            is_completed=is_completed,
        )

    @atomic()
    async def update_mission_progress(self, user_id: str) -> None:

        user, user_missions, missions = await asyncio.gather(
            User.get_user_info_by_user_id(user_id=user_id),
            self.get_user_missions(user_id=user_id),
            MissionInventory.all(),
        )

        cheese_manager_id = user.cheese_manager_id
        mission_dict = {mission.mission_code: mission for mission in missions}

        badge_missions, lv_up_mission, daily_missions = await self._classify_missions(user_missions)

        await asyncio.gather(
            *[self._process_mission(mission, mission_dict, cheese_manager_id, user_id) for mission in badge_missions],
            *[self._process_mission(mission, mission_dict, cheese_manager_id, user_id) for mission in daily_missions],
        )

        if lv_up_mission[0]:
            await self._process_mission(lv_up_mission[0], mission_dict, cheese_manager_id, user_id)

    async def _process_mission(
        self,
        user_mission: UserMissionDTO,
        mission_dict: dict[str, MissionInventory],
        cheese_manager_id: int,
        user_id: str,
    ) -> None:
        mission = mission_dict.get(user_mission.mission_code)

        if user_mission.is_completed or not mission:
            return

        increment = await self.evaluate_mission_condition(user_id, user_mission.mission_code)
        user_mission.progress_count += increment

        if user_mission.progress_count >= mission.target_count and not user_mission.is_completed:
            user_mission.is_completed = True
            await self._update_user_mission_progress(
                user_id=user_id,
                mission_code=user_mission.mission_code,
                new_progress_count=user_mission.progress_count,
                is_completed=user_mission.is_completed,
            )
            await self._handle_mission_reward(
                user_id=user_id,
                mission_code=user_mission.mission_code,
                reward_code=mission.reward_code,
                cheese_manager_id=cheese_manager_id,
            )

    async def _handle_mission_reward(
        self,
        user_id: str,
        mission_code: str,
        reward_code: str,
        cheese_manager_id: int,
    ) -> None:
        if mission_code == MS.DAILY_POST_GENERAL:
            await self.reward_daily_post(user_id=user_id, cheese_manager_id=cheese_manager_id)
        elif mission_code == MS.LV_UP:
            await self.reward_level_up_mission(
                user_id=user_id, cheese_manager_id=cheese_manager_id, reward_code=reward_code
            )
        elif mission_code.startswith(MS.BADGE):
            await self.reward_badge_mission(
                user_id=user_id, cheese_manager_id=cheese_manager_id, reward_code=reward_code
            )
        else:
            await self.reward_mission(
                user_id=user_id,
                cheese_manager_id=cheese_manager_id,
                reward_code=reward_code,
            )

    async def evaluate_mission_condition(self, user_id: str, mission_code: str) -> int:
        if mission_code == MS.BADGE_POST_FIRST and await self.check_first_post(user_id):
            return 1
        elif mission_code == MS.BADGE_POST_280_CHAR and await self.check_long_answer(user_id):
            return 1
        elif mission_code == MS.BADGE_POST_CONSECUTIVE_7 and await self.check_consecutive_days(user_id):
            return 1
        elif mission_code == MS.BADGE_POST_EARLY_3 and await self.check_early_morning_posts(user_id):
            return 1
        elif mission_code == MS.BADGE_CHEESE_TOTAL_50 and await self.check_cheese_total(user_id):
            return 1
        elif mission_code == MS.BADGE_CHRISTMAS and await self.check_christmas_period():
            return 1
        elif mission_code == MS.DAILY_LIKE_3_PER_DAY and await self.check_three_likes_different_posts(user_id):
            return 1
        elif mission_code == MS.DAILY_POST_GENERAL and await self.check_daily_post(user_id):
            return 1
        elif mission_code == MS.LV_UP and await LevelService.level_up(user_id=user_id):
            return 1
        return 0

    @staticmethod
    async def _classify_missions(
        user_missions: list[UserMissionDTO],
    ) -> tuple[list[UserMissionDTO], list[UserMissionDTO], list[UserMissionDTO]]:
        badge_missions = [mission for mission in user_missions if mission.mission_code.startswith(MS.BADGE)]
        lv_up_mission = [mission for mission in user_missions if mission.mission_code == MS.LV_UP]
        daily_missions = [mission for mission in user_missions if mission.mission_code.startswith(MS.DAILY)]
        return badge_missions, lv_up_mission, daily_missions

    @staticmethod
    async def check_first_post(user_id: str) -> bool:
        return await Answer.get_answer_count_by_user_id_v2(user_id=user_id) > 0

    @staticmethod
    async def get_answer_count(user_id: str) -> int:
        return await Answer.get_answer_count_by_user_id_v2(user_id=user_id)

    @staticmethod
    async def check_post_count_range(answer_count: int, min_count: int, max_count: int) -> bool:
        return min_count <= answer_count <= max_count

    @staticmethod
    async def check_long_answer(user_id: str) -> bool:
        recent_answer = await Answer.get_most_recent_answer_by_user_id(user_id=user_id)
        return len(recent_answer.content) >= 280 if recent_answer else False

    @staticmethod
    async def check_consecutive_days(user_id: str) -> bool:
        consecutive_days = await AnswerService.get_answer_record(user_id)
        return consecutive_days >= 7

    @staticmethod
    async def check_early_morning_posts(user_id: str) -> bool:
        recent_answer = await Answer.get_most_recent_answer_by_user_id(user_id=user_id)
        return 0 <= recent_answer.created_time.hour <= 5 if recent_answer else False

    @staticmethod
    async def check_cheese_total(user_id: str) -> bool:
        user = await User.get_user_info_by_user_id(user_id=user_id)
        cheese_amount = await CheeseManager.get_total_cheese_amount_by_manager(cheese_manager_id=user.cheese_manager_id)

        return cheese_amount >= 50

    @staticmethod
    async def check_christmas_period() -> bool:
        # 현재 시간 한국 시간(KST) 기준
        now = datetime.now(timezone(timedelta(hours=9)))

        start_date = datetime(2024, 12, 23, 6, 0, tzinfo=timezone(timedelta(hours=9)))
        end_date = datetime(2024, 12, 28, 5, 59, tzinfo=timezone(timedelta(hours=9)))

        return start_date <= now <= end_date

    @staticmethod
    async def check_three_likes_different_posts(user_id: str) -> bool:
        like_count = await Like.get_unique_likes_today(user_id)
        return like_count >= 3

    @staticmethod
    async def check_daily_post(user_id: str) -> bool:
        now = datetime.now(settings.db_zoneinfo)
        current_date = (now - timedelta(days=1)).date() if now.hour < 6 else now.date()
        answer = await Answer.get_most_recent_answer_by_user_id(user_id=user_id)
        return answer.date == current_date if answer else False

    @staticmethod
    async def validate_reward(reward_code: str):  # type: ignore
        try:
            reward = await RewardInventory.filter(reward_code=reward_code).prefetch_related("item_inventories").first()

            if not reward:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found.")

            item_inventory_rewards = reward.item_inventories

            return item_inventory_rewards

        except DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reward not found.")

    async def process_reward(
        self,
        item_inventory_rewards: list[ItemInventoryRewardInventory],
        user_id: str,
        cheese_manager_id: int,
    ) -> RewardDTO:
        total_cheese = 0
        total_exp = 0
        badge_info = []

        for item_inventory_reward in item_inventory_rewards:
            item: ItemInventory = await item_inventory_reward.item_inventory
            quantity = item_inventory_reward.quantity

            if item.item_category == ItemCategory.BADGE:
                for _ in range(quantity):
                    await Badge.create_by_user_id(user_id=user_id, badge_code=item.item_code)
                    badge = await BadgeInventory.get_by_badge_code(badge_code=item.item_code)
                    badge_info.append(badge)

            elif item.item_category == ItemCategory.COLOR:
                for _ in range(quantity):
                    await Color.create_by_user_id(user_id=user_id, color_code=item.item_code)
            elif item.item_category == ItemCategory.CHEESE:
                total_cheese += quantity
                await CheeseManager.add_cheese(cheese_manager_id=cheese_manager_id, amount=quantity)
            elif item.item_category == ItemCategory.POINT:
                total_exp += quantity
                await LevelService.add_exp(user_id=user_id, exp=quantity)
            else:
                raise ValueError(f"Invalid item category for reward: {item.item_category}")

        badge_full_name = badge_info[0].badge_full_name if badge_info else None
        badge_code = badge_info[0].badge_code if badge_info else None

        return RewardDTO(
            total_cheese=total_cheese,
            total_exp=total_exp,
            badge_full_name=badge_full_name,
            badge_code=badge_code,
        )

    async def reward_daily_post(self, user_id: str, cheese_manager_id: int) -> None:
        # 1. 경험치 및 치즈 계산
        exp, cheese, consecutive_date = await self._calculate_exp_and_cheese(user_id)

        # 2. 경험치와 치즈 추가
        await self._add_exp_and_cheese(user_id, cheese_manager_id, exp, cheese)

        # 3. 보상 알림 생성
        await self._create_reward_notice(
            user_id=user_id,
            reward_type=RewardType.DAILY_MISSION,
            total_exp=exp,
            total_cheese=cheese,
        )

    async def _calculate_exp_and_cheese(self, user_id: str) -> tuple[int, int, int]:
        # 1. 연속 답변 포인트 계산
        consecutive_date = await AnswerService.calculate_consecutive_answer_points(user_id=user_id)

        # 2. 경험치 계산
        exp = await self._calculate_exp(user_id, consecutive_date)

        # 3. 치즈 계산
        cheese = await self._calculate_cheese(consecutive_date)

        return exp, cheese, consecutive_date

    async def _calculate_exp(self, user_id: str, consecutive_date: int) -> int:
        exp = 0

        answer_count = await self.get_answer_count(user_id=user_id)

        if answer_count == 1:
            exp += 10
        elif await self.check_post_count_range(answer_count, 2, 5):
            exp += 5

        exp += consecutive_date

        return exp

    @staticmethod
    async def _calculate_cheese(consecutive_date: int) -> int:
        cheese = 0

        if consecutive_date == 0:
            cheese = 0
        elif 2 <= consecutive_date <= 5:
            cheese = 1
        elif 5 <= consecutive_date <= 8:
            cheese = 2
        elif consecutive_date >= 9:
            cheese = 3

        return cheese

    @staticmethod
    async def _add_exp_and_cheese(user_id: str, cheese_manager_id: int, exp: int, cheese: int) -> None:
        # 경험치 추가
        await LevelService.add_exp(user_id=user_id, exp=exp)

        # 치즈 추가
        await CheeseManager.add_cheese(cheese_manager_id=cheese_manager_id, amount=cheese)

    @staticmethod
    async def _create_reward_notice(
        user_id: str,
        reward_type: str,
        total_exp: int,
        total_cheese: int,
        badge_full_name: str | None = None,
        badge_code: str | None = None,
        level_up: bool = False,
        nickname: str | None = None,
        new_level: int | None = None,
    ) -> None:
        await NoticeService.create_reward_notice(
            user_id=user_id,
            reward_type=reward_type,
            total_cheese=total_cheese,
            total_exp=total_exp,
            badge_full_name=badge_full_name,
            badge_code=badge_code,
            level_up=level_up,
            nickname=nickname,
            new_level=new_level,
        )

    async def reward_level_up_mission(self, user_id: str, cheese_manager_id: int, reward_code: str) -> None:
        item_inventory_rewards = await self.validate_reward(reward_code=reward_code)
        reward_dto = await self.process_reward(
            item_inventory_rewards=item_inventory_rewards,
            user_id=user_id,
            cheese_manager_id=cheese_manager_id,
        )
        level_info = await LevelService.get_level_info_add_answer_days(user_id)
        user_profile = await User.get_user_profile_by_user_id(user_id=user_id)

        nickname = user_profile.nickname
        level = level_info.levelDto.level

        await self._create_reward_notice(
            user_id=user_id,
            reward_type=RewardType.LEVEL_UP,
            total_exp=reward_dto.total_exp,
            total_cheese=reward_dto.total_cheese,
            level_up=True,
            nickname=nickname,
            new_level=level,
        )

    async def reward_badge_mission(self, user_id: str, cheese_manager_id: int, reward_code: str) -> None:
        item_inventory_rewards = await self.validate_reward(reward_code=reward_code)
        reward_dto = await self.process_reward(
            item_inventory_rewards=item_inventory_rewards,
            user_id=user_id,
            cheese_manager_id=cheese_manager_id,
        )
        await self._create_reward_notice(
            user_id=user_id,
            reward_type=RewardType.BADGE_MISSION,
            total_exp=reward_dto.total_exp,
            total_cheese=reward_dto.total_cheese,
            badge_code=reward_dto.badge_code,
            badge_full_name=reward_dto.badge_full_name,
        )

    async def reward_mission(self, user_id: str, cheese_manager_id: int, reward_code: str) -> None:
        item_inventory_rewards = await self.validate_reward(reward_code=reward_code)
        reward_dto = await self.process_reward(
            item_inventory_rewards=item_inventory_rewards,
            user_id=user_id,
            cheese_manager_id=cheese_manager_id,
        )
        await self._create_reward_notice(
            user_id=user_id,
            reward_type=RewardType.DAILY_MISSION,
            total_exp=reward_dto.total_exp,
            total_cheese=reward_dto.total_cheese,
        )

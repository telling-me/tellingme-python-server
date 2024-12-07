import asyncio
from datetime import datetime, timedelta, timezone, date

from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist
from tortoise.transactions import atomic

from app.v2.answers.models.answer import Answer
from app.v2.answers.services.answer_service import AnswerService
from app.v2.badges.services.badge_service import BadgeService
from app.v2.cheese_managers.services.cheese_service import CheeseService
from app.v2.colors.services.color_service import ColorService
from app.v2.items.models.item import ItemInventory, ItemInventoryRewardInventory, RewardInventory
from app.v2.levels.services.level_service import LevelService
from app.v2.likes.models.like import Like
from app.v2.missions.dtos.mission_dto import UserMissionDTO
from app.v2.missions.models.mission import MissionInventory, UserMission
from app.v2.notices.services.notice_service import NoticeService
from app.v2.users.services.user_service import UserService


class MissionService:
    @staticmethod
    async def get_user_missions(user_id: str) -> list[UserMissionDTO]:
        user_mission_raw = await UserMission.get_user_missions_by_condition_type(user_id)
        return [UserMissionDTO.builder(user_mission) for user_mission in user_mission_raw]

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
            UserService.get_user_info(user_id=user_id),
            self.get_user_missions(user_id=user_id),
            MissionInventory.all(),
        )

        cheese_manager_id: int = user["cheese_manager_id"]
        mission_dict = {mission.mission_code: mission for mission in missions}

        special_mission_codes = ["MS_LV_UP"]

        regular_missions = [mission for mission in user_missions if mission.mission_code not in special_mission_codes]
        special_missions = {
            mission.mission_code: mission for mission in user_missions if mission.mission_code in special_mission_codes
        }

        results = await asyncio.gather(
            *[self._process_mission(mission, mission_dict, cheese_manager_id, user_id) for mission in regular_missions]
        )

        total_cheese, total_exp = map(sum, zip(*results))

        if "MS_LV_UP" in special_missions:
            cheese, exp = await self._process_mission(
                special_missions["MS_LV_UP"], mission_dict, cheese_manager_id, user_id
            )
            total_cheese += cheese
            total_exp += exp

        if total_cheese == 0 and total_exp == 0:
            return
        print(total_exp, total_cheese)
        await NoticeService.create_reward_notice(
            user_id=user_id, reward_type="DAILY_MISSION", total_cheese=total_cheese, total_exp=total_exp
        )

    async def _process_mission(
        self,
        user_mission: UserMissionDTO,
        mission_dict: dict[str, MissionInventory],
        cheese_manager_id: int,
        user_id: str,
    ) -> tuple[int, int]:
        mission = mission_dict.get(user_mission.mission_code)

        if user_mission.is_completed or not mission:
            return 0, 0

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
            if user_mission.mission_code == "MS_DAILY_POST_GENERAL":
                return 0, await self.reward_daily_post(
                    user_id=user_id,
                )
            else:
                return await self.reward_user_for_mission(
                    user_id=user_id,
                    reward_code=mission.reward_code,
                    cheese_manager_id=cheese_manager_id,
                )
        return 0, 0

    async def evaluate_mission_condition(self, user_id: str, mission_code: str) -> int:
        if mission_code == "MS_BADGE_POST_FIRST" and await self.check_first_post(user_id):
            return 1
        elif mission_code == "MS_SINGLE_POST_2_5" and await self.check_post_count_range(user_id, 2, 5):
            return 1
        elif mission_code == "MS_BADGE_POST_280_CHAR" and await self.check_long_answer(user_id):
            return 1
        elif mission_code == "MS_BADGE_POST_CONSECUTIVE_7" and await self.check_consecutive_days(user_id):
            return 1
        elif mission_code == "MS_BADGE_POST_EARLY_3" and await self.check_early_morning_posts(user_id):
            return 1
        elif mission_code == "MS_BADGE_CHEESE_TOTAL_50" and await self.check_cheese_total(user_id):
            return 1
        elif mission_code == "MS_BADGE_CHRISTMAS" and await self.check_christmas_period():
            return 1
        elif mission_code == "MS_DAILY_LIKE_3_PER_DAY" and await self.check_three_likes_different_posts(user_id):
            return 1
        elif mission_code == f"MS_LV_UP" and await LevelService.level_up(user_id=user_id):
            return 1
        elif mission_code == "MS_DAILY_POST_GENERAL" and await self.check_daily_post(user_id):
            return 1
        return 0

    @staticmethod
    async def check_first_post(user_id: str) -> bool:
        post_count_raw = await Answer.get_answer_count_by_user_id(user_id=user_id)
        post_count: int = post_count_raw.get("answer_count", 0)
        return post_count > 0

    @staticmethod
    async def check_post_count_range(user_id: str, min_count: int, max_count: int) -> bool:
        post_count_raw = await Answer.get_answer_count_by_user_id(user_id=user_id)
        post_count: int = post_count_raw.get("answer_count", 0)
        return min_count <= post_count <= max_count

    @staticmethod
    async def check_post_count_min(user_id: str, min_count: int) -> bool:
        post_count_raw = await Answer.get_answer_count_by_user_id(user_id=user_id)
        post_count: int = post_count_raw.get("answer_count", 0)
        return post_count >= min_count

    @staticmethod
    async def check_long_answer(user_id: str) -> bool:
        recent_answer = await Answer.get_most_recent_answer_by_user_id(user_id=user_id)
        return len(recent_answer["content"]) >= 280 if recent_answer else False

    @staticmethod
    async def check_consecutive_days(user_id: str) -> bool:
        consecutive_days = await AnswerService.get_answer_record(user_id)
        return consecutive_days >= 7

    @staticmethod
    async def check_early_morning_posts(user_id: str) -> bool:
        recent_answer = await Answer.get_most_recent_answer_by_user_id(user_id=user_id)
        if recent_answer:
            answer_time = recent_answer.get("created_time")
            return 0 <= answer_time.hour <= 5 if isinstance(answer_time, datetime) else False
        return False

    @staticmethod
    async def check_cheese_total(user_id: str) -> bool:
        user = await UserService.get_user_info(user_id=user_id)
        cheese_amount = await CheeseService.get_cheese_balance(user["cheese_manager_id"])

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
        like_raw = await Like.get_unique_likes_today(user_id)
        like_count: int = like_raw.get("unique_likes", 0)
        return like_count >= 3

    @staticmethod
    async def check_daily_post(user_id: str) -> bool:
        answer = await Answer.get_most_recent_answer_by_user_id(user_id=user_id)
        answer_date = answer.get("date")
        return answer_date == date.today()

    async def reward_user_for_mission(
        self,
        user_id: str,
        reward_code: str,
        cheese_manager_id: int,
    ) -> tuple[int, int]:
        item_inventory_rewards = await self.validate_reward(reward_code=reward_code)
        return await self.process_reward(
            item_inventory_rewards=item_inventory_rewards,
            user_id=user_id,
            cheese_manager_id=cheese_manager_id,
        )

    @staticmethod
    async def validate_reward(reward_code: str):  # type: ignore
        try:
            reward = await RewardInventory.filter(reward_code=reward_code).prefetch_related("item_inventories").first()

            if not reward:
                raise HTTPException(status_code=404, detail="Reward not found.")

            item_inventory_rewards = reward.item_inventories

            return item_inventory_rewards

        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Reward not found.")

    @staticmethod
    async def process_reward(
        item_inventory_rewards: list[ItemInventoryRewardInventory],
        user_id: str,
        cheese_manager_id: int,
    ) -> tuple[int, int]:
        total_cheese = 0
        total_exp = 0

        for item_inventory_reward in item_inventory_rewards:
            item: ItemInventory = await item_inventory_reward.item_inventory
            quantity = item_inventory_reward.quantity

            if item.item_category == "BADGE":
                for _ in range(quantity):
                    await BadgeService.add_badge(user_id=user_id, badge_code=item.item_code)
            elif item.item_category == "COLOR":
                for _ in range(quantity):
                    await ColorService.add_color(user_id=user_id, color_code=item.item_code)
            elif item.item_category == "CHEESE":
                total_cheese += quantity
                await CheeseService.add_cheese(cheese_manager_id=cheese_manager_id, amount=quantity)
            elif item.item_category == "POINT":
                total_exp += quantity
                await LevelService.add_exp(user_id=user_id, exp=quantity)
            else:
                raise ValueError(f"Invalid item category for reward: {item.item_category}")

        return total_cheese, total_exp

    @staticmethod
    async def reward_daily_post(user_id: str) -> int:
        exp = await AnswerService.calculate_consecutive_answer_points(user_id=user_id)
        await LevelService.add_exp(user_id=user_id, exp=exp)
        return exp

from fastapi import HTTPException

from app.v2.answers.services.answer_service import AnswerService
from app.v2.levels.dtos.level_dto import LevelDTO, LevelInfoDTO
from app.v2.levels.models.level import Level


class LevelService:
    @classmethod
    async def get_level_info(cls, user_id: str) -> LevelDTO:
        level_data = await Level.get_level_info(user_id=user_id)
        if level_data is None:
            raise HTTPException(status_code=404, detail="Level info not found")
        return LevelDTO.builder(level=level_data)

    @classmethod
    async def get_level_info_add_answer_days(cls, user_id: str) -> LevelInfoDTO:
        level_dto = await cls.get_level_info(user_id=user_id)

        if level_dto.requiredExp is None:
            raise ValueError("Required experience cannot be None")

        needs_to_level_up = await cls.calculate_days_to_level_up(
            user_id=user_id,
            current_exp=level_dto.currentExp,
            required_exp=level_dto.requiredExp,
        )
        return LevelInfoDTO.builder(
            level_dto=await cls.get_level_info(user_id=user_id),
            days_to_level_up=needs_to_level_up,
        )

    @classmethod
    async def level_up(cls, user_id: str) -> int:
        level_dto = await cls.get_level_info(user_id=user_id)

        level = level_dto.level
        current_exp = level_dto.currentExp
        required_exp = level_dto.requiredExp

        if current_exp is None or required_exp is None:
            raise ValueError("Experience values cannot be None")

        if current_exp >= required_exp:
            new_exp = current_exp - required_exp
            new_level = level + 1

            await Level.update_level_and_exp(user_id=user_id, new_level=new_level, new_exp=new_exp)
            return 1
        return 0

    @classmethod
    async def add_exp(cls, user_id: str, exp: int) -> None:
        level_dto = await cls.get_level_info(user_id=user_id)

        current_exp = level_dto.currentExp
        new_exp = current_exp + exp

        await Level.update_level_and_exp(user_id=user_id, new_level=level_dto.level, new_exp=new_exp)

    @classmethod
    async def calculate_days_to_level_up(cls, user_id: str, current_exp: int, required_exp: int) -> int:
        remaining_exp = required_exp - current_exp
        days_needed = 0

        answer_count = await AnswerService.get_answer_count(user_id=user_id)
        bonus_points = await AnswerService.calculate_consecutive_answer_points(user_id=user_id)

        while remaining_exp > 0:
            if answer_count == 1:
                calculated_points = 10 + bonus_points
            elif 2 <= answer_count <= 5:
                calculated_points = 5 + bonus_points
            else:
                calculated_points = 1 + bonus_points

            remaining_exp -= calculated_points

            days_needed += 1

            answer_count += 1
            bonus_points = min(bonus_points + 1, 10)

        return days_needed

from datetime import datetime, timedelta

from app.core.configs import settings
from app.models.answer import Answer


class AnswerService:

    @classmethod
    async def create_answer(
        cls,
        user_id: str,
        content: str,
        date: str,
    ) -> None:
        await Answer.create_answer(
            user_id=user_id,
            content=content,
            date=date,
        )

    @classmethod
    async def get_answer_count(cls, user_id: str) -> int:
        """
        과거부터 현재까지 총 답변 수
        """
        return await Answer.get_answer_count_by_user_id(user_id=user_id)

    @classmethod
    async def get_answer_record(cls, user_id: str) -> int:
        now = datetime.now(settings.db_zoneinfo)

        if now.hour < 6:
            now -= timedelta(days=1)

        end_date = now
        start_date = end_date - timedelta(days=100)

        all_answers = await Answer.get_all_by_user_id(user_id, start_date, end_date)

        record = 0
        target_date = end_date

        if all_answers:
            for answer in all_answers:
                answer_date = answer.date

                if answer_date == target_date.date():  # 날짜만 비교
                    record += 1
                    target_date = target_date - timedelta(days=1)
                else:
                    break

        return record

    @classmethod
    async def calculate_consecutive_answer_points(cls, user_id: str) -> int:
        return min(await cls.get_answer_record(user_id=user_id), 10)

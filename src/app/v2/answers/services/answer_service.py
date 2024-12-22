from datetime import datetime, timedelta
from typing import Any

import pytz

from app.v2.answers.models.answer import Answer


class AnswerService:
    @classmethod
    async def get_answer_count(cls, user_id: str) -> int:
        """
        과거부터 현재까지 총 답변 수
        """
        answer_count_raw = await Answer.get_answer_count_by_user_id(user_id=user_id)
        if answer_count_raw is None:
            return 0
        return int(answer_count_raw.get("answer_count", 0))

    @classmethod
    async def get_answer_count_v2(cls, user_id: str) -> int:
        """
        v2 이후 총 답변 수
        """
        answer_count_raw = await Answer.get_answer_count_by_user_id_v2(user_id=user_id)
        if answer_count_raw is None:
            return 0
        return int(answer_count_raw.get("answer_count", 0))

    @classmethod
    async def get_answer_record(cls, user_id: str) -> int:

        seoul_tz = pytz.timezone("Asia/Seoul")
        now = datetime.now(seoul_tz)

        if now.hour < 6:
            now -= timedelta(days=1)

        end_date = now
        start_date = end_date - timedelta(days=100)

        all_answers = await Answer.find_all_by_user(user_id, start_date, end_date)

        record = 0
        target_date = end_date

        if all_answers:
            for answer in all_answers:
                answer_date = answer["date"]

                if answer_date == target_date.date():  # 날짜만 비교
                    record += 1
                    target_date = target_date - timedelta(days=1)
                else:
                    break

        return record

    @classmethod
    async def calculate_consecutive_answer_points(cls, user_id: str) -> int:
        return min(await cls.get_answer_record(user_id=user_id), 10)

    @classmethod
    async def get_most_recent_answer(cls, user_id: str) -> Any:
        answer = await Answer.get_most_recent_answer_by_user_id(user_id=user_id)
        if answer == 0:
            return {}
        return answer

from datetime import datetime, timedelta

from app.v2.answers.models.answer import Answer


class AnswerService:
    @classmethod
    async def get_answer_count(cls, user_id: str) -> int:
        answer_count_raw = await Answer.get_answer_count_by_user_id(user_id=user_id)
        return answer_count_raw["answer_count"]

    @classmethod
    async def get_answer_record(cls, user_id: str) -> int:
        end_date = datetime.now()
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

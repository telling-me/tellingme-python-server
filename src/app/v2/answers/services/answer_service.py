from datetime import datetime, timedelta

from app.v2.answers.dtos.answer_dto import RecordDto
from app.v2.answers.models.answer import Answer


class AnswerService:
    @classmethod
    async def get_answer_count(cls, user_id: str) -> int:
        answer_count_raw = await Answer.get_answer_count_by_user_id(user_id=user_id)
        return answer_count_raw["answer_count"]

    @classmethod
    async def get_answer_record(cls, user_id: str) -> "RecordDto":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=100)

        all_answers = await Answer.find_all_by_user(user_id, start_date, end_date)

        record = 0
        target_date = end_date

        if all_answers:
            for answer in all_answers:
                answer_date = answer["date"]  # 답변의 날짜를 가져옴
                if answer_date == target_date:
                    record += 1
                    target_date = target_date - timedelta(days=1)
                else:
                    break

        return RecordDto.builder(count=record)

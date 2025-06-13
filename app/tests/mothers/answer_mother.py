from app.services.answer_service import AnswerService


class AnswerMother:

    @staticmethod
    async def create_answer(
        user_id: str,
        date: str,
        content: str = "-",
        likes: int = 0,
    ) -> None:
        answer_service = AnswerService()
        await answer_service.create_answer(user_id=user_id, content=content, date=date, like_count=likes)

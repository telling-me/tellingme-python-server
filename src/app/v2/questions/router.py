from fastapi import APIRouter, HTTPException

from app.v2.questions.models.question import Question

router = APIRouter(prefix="/question", tags=["Question"])


# @router.get("/questions/{date}")
# async def get_question_by_date(date: str):
#     question = await Question.get_or_none(date=date)
#     if question is None:
#         raise HTTPException(status_code=404, detail="Question not found")
#     return question

from fastapi import APIRouter

from app.v2.answers.services.answer_service import AnswerService

router = APIRouter(prefix="/answer", tags=["Test용"])


# FastAPI 비동기 뷰
@router.get("")
async def get_answer_record_view():
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"
    record_dto = await AnswerService.get_answer_record(user_id)
    return {"user_id": user_id, "consecutive_answer_days": record_dto.count}

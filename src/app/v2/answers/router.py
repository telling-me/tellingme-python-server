from fastapi import APIRouter

from app.v2.levels.services.level_service import LevelService

router = APIRouter(prefix="/answer", tags=["Test용"])


# FastAPI 비동기 뷰


@router.get("/level-up")
async def level_up_handler() -> int:
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"
    result = await LevelService.level_up(user_id=user_id)
    return result


@router.get("/add-exp")
async def add_exp_handler() -> None:
    user_id = "180a4e40-62f8-46be-b1eb-e7e3dd91cddf"
    await LevelService.add_exp(user_id=user_id, exp=100)

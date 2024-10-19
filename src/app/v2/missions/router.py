from fastapi import APIRouter

router = APIRouter(prefix="/mission", tags=["Mission"])


@router.post("/level")
def level_up_handler():
    pass

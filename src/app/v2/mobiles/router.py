from fastapi import APIRouter

router = APIRouter(prefix="/mobiles", tags=["Mobile"])


@router.post("/main")
async def mobile_main_handler():
    pass


@router.get("/tellercard")
async def mobile_teller_card_handler():
    pass


@router.get("/mypage")
async def mobile_my_page_handler():
    pass

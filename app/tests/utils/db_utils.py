from app.models.badge_inventory import BadgeInventory
from app.models.color_inventory import ColorInventory
from app.models.emotion_inventory import EmotionInventory


async def reset_inventory_tables() -> None:
    """
    인벤토리 관련 테이블 초기화 함수
    테스트 시 중복 데이터로 인한 충돌 방지를 위해 사용
    """
    await BadgeInventory.all().delete()
    await ColorInventory.all().delete()
    await EmotionInventory.all().delete()

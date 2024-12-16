from enum import Enum


class CheeseStatus(Enum):
    CAN_USE = "CAN_USE"  # 치즈 사용 가능
    USING = "USING"  # 치즈 사용 중
    ALREADY_USED = "ALREADY_USED"  # 치즈 사용 완료

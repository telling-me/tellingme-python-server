from enum import Enum


class ErrorCode(Enum):
    NOT_ENOUGH_CHEESE = (4003, "치즈가 부족하여 구매를 진행할 수 없습니다.")
    INVALID_ITEM_CATEGORY = (4004, "치즈 결제에 유효하지 않은 아이템 카테고리입니다.")
    INVALID_TRANSACTION_CURRENCY = (4001, "결제에 유효하지 않은 거래 통화입니다.")
    DUPLICATE_PURCHASE = (4005, "이미 소유한 제품입니다.")

    # 404 Not Found
    NO_INVENTORY_FOR_PRODUCT = (4041, "이 상품에 대한 재고가 없습니다.")
    PRODUCT_NOT_FOUND = (4042, "해당 상품을 찾을 수 없습니다.")

    NO_VALID_RECEIPT = (4006, "유효한 영수증이 없습니다.")

    def __init__(self, code: int, message: str) -> None:
        self._code = code
        self._message = message

    @property
    def code(self) -> int:
        return self._code

    @property
    def message(self) -> str:
        return self._message

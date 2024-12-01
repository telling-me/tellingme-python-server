from enum import Enum


class PurchaseStatus(Enum):
    AVAILABLE = "AVAILABLE"
    CONSUMED = "CONSUMED"
    EXPIRED = "EXPIRED"
    REFUNDED = "REFUNDED"
    CANCELED = "CANCELED"


class SubscriptionStatus(Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    CANCELED = "CANCELED"


purchase_mapping = {
    "tellingme.plus.oneMonth": "PD_PLUS_MONTH_1_KR",
    "tellingme.plus.oneYear": "PD_PLUS_YEAR_1_KR",
}

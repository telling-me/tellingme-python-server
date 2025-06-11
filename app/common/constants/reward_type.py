from enum import Enum


class RewardType(str, Enum):
    DAILY_MISSION = "DAILY_MISSION"
    LEVEL_UP = "LEVEL_UP"
    BADGE_MISSION = "BADGE_MISSION"

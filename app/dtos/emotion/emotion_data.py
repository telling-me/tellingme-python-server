import dataclasses


@dataclasses.dataclass(frozen=True)
class EmotionData:
    emotion_code: str
    emotion_name: str

from fastapi import status

from app.common.constants.emotion_dict import EMOTION_DICT
from app.tests.mothers.emotion_mother import EmotionMother
from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_get_emotions(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    emotion_mother = EmotionMother()

    user_id = await user_mother.create_user()
    await emotion_mother.create_emotion_inventory()

    # 기본 감정
    expected_emotion_ids = [
        EMOTION_DICT["EM_HAPPY"],
        EMOTION_DICT["EM_PROUD"],
        EMOTION_DICT["EM_OKAY"],
        EMOTION_DICT["EM_TIRED"],
        EMOTION_DICT["EM_SAD"],
        EMOTION_DICT["EM_ANGRY"],
    ]

    # When
    response = await telling_me_client.get_emotions(user_id=user_id)
    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_200_OK

    assert code == response.status_code
    assert message == "보유 감정 정보 조회"
    assert sorted(data["emotionList"]) == sorted(expected_emotion_ids)

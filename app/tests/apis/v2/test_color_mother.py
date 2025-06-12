from fastapi import status

from app.common.constants.color_code_list import ColorCodeList
from app.tests.mothers.color_mother import ColorMother
from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_get_colors(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()

    user_id = await user_mother.create_user()
    await color_mother.create_color_inventory()

    # 기본 색상
    expected_colors = [
        {"colorCode": ColorCodeList.CL_BLUE_001, "colorName": "Blue_1", "colorHexCode": "#229DF6"},
        {"colorCode": ColorCodeList.CL_DEFAULT, "colorName": "Default", "colorHexCode": "#1EDCC5"},
        {"colorCode": ColorCodeList.CL_ORANGE_001, "colorName": "Orange_1", "colorHexCode": "#FFA216"},
        {"colorCode": ColorCodeList.CL_RED_001, "colorName": "Red_1", "colorHexCode": "#ED3639"},
    ]

    # When
    response = await telling_me_client.get_colors(user_id=user_id)
    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_200_OK

    assert code == response.status_code
    assert message == "보유 색상 정보 조회"
    assert sorted(data, key=lambda x: x["colorCode"]) == sorted(expected_colors, key=lambda x: x["colorCode"])

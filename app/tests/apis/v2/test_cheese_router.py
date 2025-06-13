from fastapi import status

from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_get_cheese_amount(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()

    user_id = await user_mother.create_user()
    await user_mother.add_cheese(user_id=user_id, amount=(cheese_amount := 100))

    # When
    response = await telling_me_client.get_cheese_amount(user_id=user_id)
    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_200_OK

    assert code == response.status_code
    assert message == "총 치즈 갯수 조회"
    assert data["cheeseBalance"] == cheese_amount

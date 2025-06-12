from app.tests.telling_me_client import TellingMeClient


async def test_get_badges(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    response = await telling_me_client.get_badges(user_id="1234")
    print(response.json())

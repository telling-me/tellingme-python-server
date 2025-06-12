# from app.tests.mothers.user_mother import UserMother
# from app.tests.telling_me_client import TellingMeClient
#
#
# async def test_get_colors(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
#     user_mother = UserMother()
#     user_id = await user_mother.create_user()
#     response = await telling_me_client.get_colors(user_id=user_id)
#     print(response.json())

import asyncio
from unittest.mock import patch

from fastapi import status
from tortoise.exceptions import IntegrityError

from app.common.constants.product_code_list import ProductCodeList
from app.common.exceptions.error_code import ErrorCode
from app.dtos.payment.payment_request import PaymentRequest
from app.tests.mothers.badge_mother import BadgeMother
from app.tests.mothers.color_mother import ColorMother
from app.tests.mothers.emotion_mother import EmotionMother
from app.tests.mothers.item_mother import ItemMother
from app.tests.mothers.user_mother import UserMother
from app.tests.telling_me_client import TellingMeClient


async def test_payment_happy_case(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        item_mother.create_item_inventory_and_product_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=100),
    )

    payment_badge = PaymentRequest(user_id=user_id, productCode=ProductCodeList.PD_BG_CHRISTMAS_2024)
    payment_color = PaymentRequest(user_id=user_id, productCode=ProductCodeList.PD_CL_GREEN_001)
    payment_emotion = PaymentRequest(user_id=user_id, productCode=ProductCodeList.PD_EM_LONELY)

    # When
    payment_badge_response, payment_color_response, payment_emotion_response = await asyncio.gather(
        telling_me_client.payment_product(payment_request=payment_badge),
        telling_me_client.payment_product(payment_request=payment_color),
        telling_me_client.payment_product(payment_request=payment_emotion),
    )

    badge_response_code = payment_badge_response.json()["code"]
    badge_response_data = payment_badge_response.json()["data"]
    badge_response_message = payment_badge_response.json()["message"]

    color_response_code = payment_color_response.json()["code"]
    color_response_data = payment_color_response.json()["data"]
    color_response_message = payment_color_response.json()["message"]

    emotion_response_code = payment_emotion_response.json()["code"]
    emotion_response_data = payment_emotion_response.json()["data"]
    emotion_response_message = payment_emotion_response.json()["message"]

    # Then
    assert payment_badge_response.status_code == status.HTTP_200_OK
    assert payment_color_response.status_code == status.HTTP_200_OK
    assert payment_emotion_response.status_code == status.HTTP_200_OK

    assert badge_response_code == payment_badge_response.status_code
    assert color_response_code == payment_color_response.status_code
    assert emotion_response_code == payment_emotion_response.status_code

    assert badge_response_message == "Payment successful"
    assert color_response_message == "Payment successful"
    assert emotion_response_message == "Payment successful"

    assert badge_response_data["product_code"] == ProductCodeList.PD_BG_CHRISTMAS_2024
    assert color_response_data["product_code"] == ProductCodeList.PD_CL_GREEN_001
    assert emotion_response_data["product_code"] == ProductCodeList.PD_EM_LONELY


async def test_duplicate_payment_case(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        item_mother.create_item_inventory_and_product_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=100),
    )

    payment_request = PaymentRequest(user_id=user_id, productCode=ProductCodeList.PD_BG_CHRISTMAS_2024)

    # When
    with patch("app.models.badge.Badge.create_by_user_id", side_effect=IntegrityError("mock integrity error")):
        response = await telling_me_client.payment_product(payment_request=payment_request)

    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert code == ErrorCode.DUPLICATE_PURCHASE.code
    assert message == ErrorCode.DUPLICATE_PURCHASE.message
    assert data is None


async def test_payment_when_cheese_is_insufficient(
    telling_me_client: TellingMeClient, init_tortoise_connection: None
) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        item_mother.create_item_inventory_and_product_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=0),
    )

    payment_request = PaymentRequest(user_id=user_id, productCode=ProductCodeList.PD_BG_CHRISTMAS_2024)

    # When
    response = await telling_me_client.payment_product(payment_request=payment_request)

    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert code == ErrorCode.NOT_ENOUGH_CHEESE.code
    assert message == ErrorCode.NOT_ENOUGH_CHEESE.message
    assert data is None


async def test_payment_when_not_cheese_payment(
    telling_me_client: TellingMeClient, init_tortoise_connection: None
) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        item_mother.create_item_inventory_and_product_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=100),
    )

    # 현금 구매 제품
    payment_request = PaymentRequest(user_id=user_id, productCode=ProductCodeList.PD_PLUS_MONTH_1_KR)

    # When
    response = await telling_me_client.payment_product(payment_request=payment_request)

    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert code == ErrorCode.INVALID_TRANSACTION_CURRENCY.code
    assert message == ErrorCode.INVALID_TRANSACTION_CURRENCY.message
    assert data is None


async def test_payment_invalid_product_code(telling_me_client: TellingMeClient, init_tortoise_connection: None) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        item_mother.create_item_inventory_and_product_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=100),
    )

    payment_request = PaymentRequest(user_id=user_id, productCode="invalid_product_code")

    # When
    response = await telling_me_client.payment_product(payment_request=payment_request)

    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert code == ErrorCode.PRODUCT_NOT_FOUND.code
    assert message == ErrorCode.PRODUCT_NOT_FOUND.message
    assert data is None


async def test_payment_invalid_item_category(
    telling_me_client: TellingMeClient, init_tortoise_connection: None
) -> None:
    # Given
    user_mother = UserMother()
    color_mother = ColorMother()
    badge_mother = BadgeMother()
    emotion_mother = EmotionMother()
    item_mother = ItemMother()

    user_id = await user_mother.create_user(user_name="telling me user")

    await asyncio.gather(
        user_mother.create_level_inventory(),
        badge_mother.create_badge_inventory(),
        color_mother.create_color_inventory(),
        emotion_mother.create_emotion_inventory(),
        item_mother.create_item_inventory_and_product_inventory(),
        user_mother.add_cheese(user_id=user_id, amount=100),
    )

    payment_request = PaymentRequest(user_id=user_id, productCode=ProductCodeList.PD_TEST)

    # When
    response = await telling_me_client.payment_product(payment_request=payment_request)

    code = response.json()["code"]
    data = response.json()["data"]
    message = response.json()["message"]

    # Then
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    assert code == ErrorCode.NO_INVENTORY_FOR_PRODUCT.code
    assert message == ErrorCode.NO_INVENTORY_FOR_PRODUCT.message
    assert data is None

import httpx

from app.dtos.payment.payment_request import PaymentRequest
from app.dtos.teller_card.teller_card_request import TellerCardRequest


class TellingMeClient:
    def __init__(self, httpx_client: httpx.AsyncClient):
        """
        테스트 중 API 호출은 본 클래스를 통합니다.
        모든 public 메소드들은 알파벳 순으로 정렬합시다.
        """
        self._client = httpx_client

    async def get_mobile_my_page(self, user_id: str) -> httpx.Response:
        return await self._client.get(
            "/api/v2/mobiles/mypage",
            params={
                key: value
                for key, value in {
                    "user_id": user_id,
                }.items()
                if value is not None
            },
        )

    async def get_mobile_teller_card(self, user_id: str) -> httpx.Response:
        return await self._client.get(
            "/api/v2/mobiles/tellercard",
            params={
                key: value
                for key, value in {
                    "user_id": user_id,
                }.items()
                if value is not None
            },
        )

    async def get_badges(self, user_id: str) -> httpx.Response:
        return await self._client.get(
            "/api/v2/user/badge",
            params={
                key: value
                for key, value in {
                    "user_id": user_id,
                }.items()
                if value is not None
            },
        )

    async def get_colors(self, user_id: str) -> httpx.Response:
        return await self._client.get(
            "/api/v2/user/color",
            params={
                key: value
                for key, value in {
                    "user_id": user_id,
                }.items()
                if value is not None
            },
        )

    async def get_emotions(self, user_id: str) -> httpx.Response:
        return await self._client.get(
            "/api/v2/user/emotion",
            params={
                key: value
                for key, value in {
                    "user_id": user_id,
                }.items()
                if value is not None
            },
        )

    async def get_cheese_amount(self, user_id: str) -> httpx.Response:
        return await self._client.get(
            "/api/v2/cheese",
            params={
                key: value
                for key, value in {
                    "user_id": user_id,
                }.items()
                if value is not None
            },
        )

    async def update_teller_card(self, teller_card_request: TellerCardRequest) -> httpx.Response:
        return await self._client.post("/api/v2/tellercard", json=teller_card_request.model_dump())

    async def payment_product(self, payment_request: PaymentRequest) -> httpx.Response:
        return await self._client.post("/api/v2/payment", json=payment_request.model_dump())

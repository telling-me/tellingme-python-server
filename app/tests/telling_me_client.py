import httpx


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

    # async def create_product(self, token: str, create_product_request: CreateProductRequest) -> httpx.Response:
    #     return await self._client.post(
    #         "/v1/products/admin", json=create_product_request.model_dump(), headers={"Authorization": f"Bearer {token}"}
    #     )

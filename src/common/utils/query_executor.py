from typing import Union

from tortoise import Tortoise


class QueryExecutor:

    @staticmethod
    async def execute_query(
        query: str, values: Union[tuple, str] = (), fetch_type: str = "multiple"
    ) -> Union[dict, list[dict], int]:
        """
        SQL 쿼리를 실행하고 결과를 반환합니다.

        :param query: 실행할 SQL 쿼리 문자열
        :param values: 쿼리에 바인딩할 값들 (tuple 또는 단일 값)
        :param fetch_type: "single"일 경우 단일 값을 반환하고, "multiple"일 경우 여러 값을 반환
        :return: 단일 값 또는 여러 값(딕셔너리 리스트)
        """
        connection = Tortoise.get_connection("default")

        if isinstance(values, tuple):
            values = tuple(v[0] if isinstance(v, tuple) else v for v in values)
        else:
            values = (values,)

        result = await connection.execute_query_dict(query, values)  # type: ignore

        if result and len(result) > 0:
            if fetch_type == "single":
                return result[0]  # type: ignore
            elif fetch_type == "multiple":
                return result
        return 0 if fetch_type == "single" else []

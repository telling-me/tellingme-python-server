from typing import List, Dict, Union
from tortoise import Tortoise


class QueryExecutor:

    @staticmethod
    async def execute_query(
        query: str, fetch_type: str = "multiple"
    ) -> Union[int, List[Dict]]:
        """
        SQL 쿼리를 실행하고 결과를 반환합니다.

        :param query: 실행할 SQL 쿼리 문자열
        :param fetch_type: "single"일 경우 단일 값을 반환하고, "multiple"일 경우 여러 값을 반환
        :return: 단일 값 또는 여러 값(딕셔너리 리스트)
        """
        connection = Tortoise.get_connection("default")
        try:
            result = await connection.execute_query(query)

            if result and len(result[1]) > 0:
                if fetch_type == "single":
                    return result[1][0].get(list(result[1][0].keys())[0], 0)
                elif fetch_type == "multiple":
                    return result[1]
            return 0 if fetch_type == "single" else []

        finally:
            await connection.close()

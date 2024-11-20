from typing import Union


class QueryFormatter:
    @staticmethod
    def format(query_template: str, values: Union[str, list, tuple]) -> str:
        """
        쿼리 템플릿과 단일 값 또는 리스트/튜플 형태의 값을 받아 SQL 쿼리를 포맷팅하는 메서드 (%s 사용)

        :param query_template: SQL 쿼리 템플릿
        :param values: 단일 값 또는 리스트/튜플
        :return: 포맷팅된 SQL 쿼리
        """
        # 단일 값일 경우 문자열 포맷팅 처리
        if isinstance(values, (list, tuple)):
            formatted_values = tuple(f"'{value}'" if isinstance(value, str) else value for value in values)
            return query_template % formatted_values
        else:
            # 단일 문자열일 경우 따옴표 추가
            formatted_value = f"'{values}'" if isinstance(values, str) else values
            return query_template % formatted_value

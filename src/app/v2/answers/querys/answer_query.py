from app.v2.users.querys.user_query import USER_ID_QUERY

SELECT_ANSWER_COUNT_BY_USER_UUID_QUERY = (
    f"SELECT COUNT(*) as answer_count FROM answer WHERE {USER_ID_QUERY}"
)

SELECT_ANSWER_BY_USER_UUID_QUERY = f"""
    SELECT * FROM answer
    WHERE {USER_ID_QUERY}
    AND date BETWEEN %s AND %s
    ORDER BY date DESC
    """

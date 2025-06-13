from app.queries.user_query import USER_ID_QUERY

SELECT_EMOTION_CODE_BY_USER_UUID_QUERY = f"""
    SELECT e.emotion_code, ei.emotion_name
    FROM emotion e
    JOIN emotion_inventory ei
    ON e.emotion_code = ei.emotion_code
    WHERE {USER_ID_QUERY}
    """

INSERT_EMOTION_CODE_FOR_USER_QUERY = f"""
    INSERT INTO emotion (emotion_code, user_id)
    SELECT %s, user_id
    FROM user
    WHERE {USER_ID_QUERY}
    """

from app.v2.users.querys.user_query import USER_ID_QUERY

SELECT_COLOR_CODE_BY_USER_UUID_QUERY = f"""
    SELECT color_code 
    FROM color 
    WHERE {USER_ID_QUERY}
"""

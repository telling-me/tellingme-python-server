USER_ID_QUERY = "user_id = UNHEX(REPLACE(%s, '-', ''))"

SELECT_USER_BY_UUID_QUERY = f"SELECT * FROM user WHERE {USER_ID_QUERY} LIMIT 1"

SELECT_USER_PROFILE_BY_USER_ID_QUERY = f"""
    SELECT 
        u.nickname,
        u.is_premium,
        u.cheese_manager_id
    FROM user u
    WHERE {USER_ID_QUERY}
"""

SELECT_USER_INFO_BY_USER_UUID_QUERY = f"""
    SELECT 
        u.nickname,
        u.cheese_manager_id
    FROM user u
    WHERE {USER_ID_QUERY}
"""

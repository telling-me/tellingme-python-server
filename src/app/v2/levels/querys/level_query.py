from app.v2.users.querys.user_query import USER_ID_QUERY

SELECT_USER_LEVEL_AND_EXP_BY_USER_UUID_QUERY = f"""
    SELECT 
        l.user_exp AS level_exp, 
        l.user_level AS level_level
    FROM 
        user u
    JOIN 
        level l ON u.level_id = l.level_id
    WHERE {USER_ID_QUERY}
"""

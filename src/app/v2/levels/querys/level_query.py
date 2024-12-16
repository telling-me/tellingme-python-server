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

SELECT_USER_EXP_QUERY = f"""
SELECT li.required_exp
FROM user u
JOIN level l ON u.level_id = l.level_id
JOIN level_inventory li ON l.user_level = li.level
WHERE {USER_ID_QUERY}
LIMIT 1;
"""

UPDATE_USER_LEVEL_AND_EXP_QUERY = f"""
    UPDATE level l
    JOIN user u ON u.level_id = l.level_id
    SET l.user_level = %s, l.user_exp = %s
    WHERE {USER_ID_QUERY};
"""

SELECT_USER_LEVEL_AND_REQUIRED_EXP_QUERY = f"""
    SELECT 
        l.user_exp AS level_exp,
        l.user_level AS level_level,
        li.required_exp AS required_exp
    FROM 
        user u
    JOIN 
        level l ON u.level_id = l.level_id
    JOIN 
        level_inventory li ON l.user_level = li.level
    WHERE 
        {USER_ID_QUERY}
    LIMIT 1;
"""

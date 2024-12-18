from app.v2.users.querys.user_query import USER_ID_QUERY

SELECT_BADGE_COUNT_BY_USER_UUID_QUERY = f"""
    SELECT COUNT(*) as badge_count
    FROM badge
    WHERE {USER_ID_QUERY}
"""

SELECT_BADGE_BY_USER_UUID_QUERY = f"""
    SELECT 
        b.badge_code,
        bi.badge_name,
        bi.badge_condition,
        bi.badge_middle_name
    FROM badge b
    JOIN badge_inventory bi ON b.badge_code = bi.badge_code
    WHERE {USER_ID_QUERY}
"""

SELECT_BADGE_CODE_BY_USER_UUID_QUERY = f"""
    SELECT badge_code 
    FROM badge 
    WHERE {USER_ID_QUERY}
"""
INSERT_BADGE_CODE_FOR_USER_QUERY = f"""
    INSERT INTO badge (badge_code, user_id)
    SELECT %s, user_id
    FROM user
    WHERE {USER_ID_QUERY}
 """

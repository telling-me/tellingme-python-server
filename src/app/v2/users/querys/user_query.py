USER_ID_QUERY = "user_id = UNHEX(REPLACE(%s, '-', ''))"

SELECT_USER_BY_UUID_QUERY = f"SELECT * FROM user WHERE {USER_ID_QUERY} LIMIT 1"

SELECT_USER_INFO_BY_USER_UUID_QUERY = f"""
    SELECT 
        u.nickname,
        u.cheese_balance,
        tc.activate_badge_code AS badgeCode,
        bi.badge_name AS badgeName,
        bi.badge_middle_name AS badgeMiddleName,
        tc.activate_color_code AS colorCode
    FROM user u
    JOIN teller_card tc ON u.teller_card_id = tc.teller_card_id
    JOIN badge_inventory bi ON tc.activate_badge_code = bi.badge_code
    WHERE {USER_ID_QUERY}
"""

SELECT_USER_LEVEL_AND_EXP_BY_USER_UUID_QUERY = f"""
    SELECT 
        user_level AS level, 
        user_exp AS current_exp 
    FROM user 
    WHERE {USER_ID_QUERY}
"""

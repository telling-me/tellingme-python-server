from app.v2.users.querys.user_query import USER_ID_QUERY

SELECT_TELLER_CARD_INFO_BY_USER_UUID_QUERY = f"""
    SELECT 
        tc.activate_badge_code AS badgeCode,
        bi.badge_name AS badgeName,
        bi.badge_middle_name AS badgeMiddleName,
        tc.activate_color_code AS colorCode
    FROM teller_card tc
    JOIN badge_inventory bi ON tc.activate_badge_code = bi.badge_code
    WHERE tc.teller_card_id = (
        SELECT u.teller_card_id 
        FROM user u 
        WHERE {USER_ID_QUERY}
    )
"""

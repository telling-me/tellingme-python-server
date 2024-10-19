from app.v2.users.querys.user_query import USER_ID_QUERY

SELECT_TELLER_CARD_INFO_BY_USER_UUID_QUERY = f"""
    SELECT 
        tc.activate_badge_code,
        bi.badge_name,
        bi.badge_middle_name,
        tc.activate_color_code
    FROM teller_card tc
    JOIN badge_inventory bi ON tc.activate_badge_code = bi.badge_code
    WHERE tc.teller_card_id = (
        SELECT u.teller_card_id 
        FROM user u 
        WHERE {USER_ID_QUERY}
    )
"""

PATCH_TELLER_CARD_QUERY = """
    UPDATE teller_card
    SET activate_badge_code = %s, activate_color_code = %s
    WHERE teller_card_id = (
        SELECT u.teller_card_id
        FROM user u
        WHERE {USER_ID_QUERY}
    )
"""

GET_UPDATED_TELLER_CARD_QUERY = """
    SELECT activate_badge_code AS badgeCode, activate_color_code AS colorCode
    FROM teller_card
    WHERE teller_card_id = (
        SELECT u.teller_card_id
        FROM user u
        WHERE {USER_ID_QUERY}
    )
"""
PATCH_TELLER_CARD_BY_USER_UUID_QUERY = PATCH_TELLER_CARD_QUERY.format(
    USER_ID_QUERY=USER_ID_QUERY
)

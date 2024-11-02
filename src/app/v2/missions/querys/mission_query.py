from app.v2.users.querys.user_query import USER_ID_QUERY

SELECT_USER_MISSIONS_BY_CONDITION_TYPE_QUERY = f"""
    SELECT um.*
    FROM user_mission um
    JOIN mission_inventory mi ON um.mission_code = mi.mission_code
    WHERE um.{USER_ID_QUERY} AND mi.condition_type = %s
"""

UPDATE_USER_MISSION_PROGRESS_QUERY = """
    UPDATE user_mission
    SET progress_count = %s, is_completed = %s
    WHERE user_id = UNHEX(REPLACE(%s, '-', ''))
      AND mission_code = %s
"""

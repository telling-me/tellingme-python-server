SELECT_UNIQUE_LIKES_COUNT_BY_USER_TODAY_QUERY = """
    SELECT COUNT(DISTINCT answer_id) AS unique_likes
    FROM likes
    WHERE user_id = UNHEX(REPLACE(%s, '-', ''))
      AND created_time >= DATE_ADD(CURDATE(), INTERVAL 6 HOUR)
      AND created_time < DATE_ADD(CURDATE(), INTERVAL 30 HOUR);
"""

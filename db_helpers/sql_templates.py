CHECK_USER_IN_DB_TEMPLATE = """
    select exists (
    select 1 from users where user_id = {}
    ) 
"""

GET_CURRENT_LOCALE_FOR_USER_TEMPLATE = """
    select language from users where user_id = {}
"""

GET_DATA_FOR_PROFILE_KEYBOARD_TEMPLATE = """
    select json_build_object(
        'temperature', temperature, 
        'language', language
    ) from users where user_id = {}
"""

GET_TEMPERATURE_FOR_USER_TEMPLATE = """
    select json_build_object(
        'temperature', temperature
    ) from users where user_id = {}
"""

INSERT_NEW_USER_IN_DB_TEMPLATE = """
    INSERT INTO users VALUES(
    {}, {}, {}, {}, {}, {}, current_timestamp
    )
"""

INSERT_NEW_SUB_INFO_IN_DB_TEMPLATE = """
    INSERT INTO sub_info VALUES(
    {}, 0, current_timestamp, NOW() + interval '7 days', 0, {}
    )
"""

UPDATE_LOCALE_FOR_USER_TEMPLATE = """
    UPDATE users SET language='{}' WHERE user_id = {}
"""

UPDATE_TEMPERATURE_FOR_USER_TEMPLATE = """
    UPDATE users SET temperature='{}' WHERE user_id = {}
"""

GET_ACTIVITY_AND_TOKENS_FOR_USER = """
    select json_build_object(
        'activity_status', activity_status, 
        'tokens', tokens
    ) from sub_info where user_id = {}
"""

GET_TOKENS_FOR_USER_TEMPLATE = """
    select json_build_object(
        'tokens', tokens
    ) from sub_info where user_id = {}
"""


GET_INFO_FOR_USER_TEMPLATE = """
    select json_build_object(
        'activity_status', activity_status,
        'expired_at', expired_at,
        'tokens', tokens
    ) from sub_info where user_id = {}
"""


UPDATE_TOKENS_COUNT_FOR_USER_TEMPLATE = """
    UPDATE sub_info SET tokens={} WHERE user_id = {}
"""


UPDATE_SUBSCRIPTION_STATUS_FOR_USER_TEMPLATE = """
    UPDATE sub_info SET activity_status={}, tokens={} WHERE user_id = {}
"""


SELECT_USERS_FOR_REFRESH_DEFAULT_SUBSCRIPTION_TEMPLATE = """
    select json_agg(user_id) from sub_info
    where activity_status={}
    and expired_at <= NOW() - interval '7 days'
"""

UPDATE_DEFAULT_SUBSCRIPTION_STATUS_FOR_USER_TEMPLATE = """
    UPDATE sub_info SET tokens={}, expired_at=NOW() + interval '7 days' WHERE user_id = {}
"""
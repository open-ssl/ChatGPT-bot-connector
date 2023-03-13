CHECK_USER_IN_DB_TEMPLATE = """
    select exists (
    	select 1 from users where user_id = {}
    ) 
"""

INSERT_NEW_USER_IN_DB_TEMPLATE = """
    INSERT INTO users VALUES(
    	{}, {}, {}, {}, {}, current_timestamp
    )
"""


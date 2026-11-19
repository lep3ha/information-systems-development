SELECT
    user_id,
    user_group
FROM internal_user
WHERE
    1 = 1
    AND login = (%s)
    AND password = (%s)

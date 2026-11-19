SELECT
    user_id,
    user_group
FROM internal_user
WHERE
    login = (%s)
    AND password = (%s)

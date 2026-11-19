SELECT
    user_id AS in_id,
    username AS login,
    user_group AS role
FROM users
WHERE
    username = %(login)s
    AND password = %(pass)s

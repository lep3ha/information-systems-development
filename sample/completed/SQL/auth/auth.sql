SELECT
    user_id as in_id,
    username as login,
    user_group as role
FROM users
WHERE username = %(login)s AND password = %(pass)s
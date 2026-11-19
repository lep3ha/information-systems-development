SELECT
    user_id,
    user_group
FROM external_user
WHERE
    login = (%s)
    AND password = (%s)

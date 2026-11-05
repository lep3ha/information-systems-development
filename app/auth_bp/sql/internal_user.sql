SELECT user_id, password_hash, user_group
FROM internal_user
WHERE login = %s;

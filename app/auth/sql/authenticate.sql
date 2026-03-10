SELECT id, username, first_name FROM users 
WHERE username = %s AND password_hash = %s;
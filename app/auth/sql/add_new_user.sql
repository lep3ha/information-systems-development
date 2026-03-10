INSERT INTO users (username, first_name, second_name, password_hash)
VALUES (%s, %s, %s, %s)
RETURNING id;

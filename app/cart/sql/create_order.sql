INSERT INTO orders (user_id)
VALUES (%s)
RETURNING id;

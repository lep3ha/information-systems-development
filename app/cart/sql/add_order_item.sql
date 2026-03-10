INSERT INTO order_items (order_id, product_id, quantity, price_per_unit)
VALUES (%s, %s, %s, %s)
RETURNING id;

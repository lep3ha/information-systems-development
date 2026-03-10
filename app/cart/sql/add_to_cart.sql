INSERT INTO cart_items (cart_id, product_id, quantity, price_at_add)
VALUES (%s, %s, %s, %s)
ON CONFLICT (cart_id, product_id)
DO UPDATE SET quantity = cart_items.quantity + EXCLUDED.quantity
RETURNING id;

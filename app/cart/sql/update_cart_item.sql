UPDATE cart_items
SET quantity = %s
WHERE id = %s
RETURNING id;

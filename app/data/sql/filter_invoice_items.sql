SELECT 
    p.sku as product_code,
    p.name,
    c.name as category,
    di.price,
    di.quantity,
    (di.price * di.quantity) as total
FROM delivery_item di
INNER JOIN product p ON di.product_id = p.id
LEFT JOIN category c ON c.id = p.category_id
WHERE di.delivery_id = {{ invoice_id }}::integer
ORDER BY p.name;
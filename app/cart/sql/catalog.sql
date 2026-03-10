-- List available warehouse items (only rows with quantity > 0)
SELECT w.product_id AS id,
       p.sku,
       p.name,
       c.name AS category,
       p.weight,
       w.purchase_price,
       w.add_value,
       w.quantity,
       (w.purchase_price * (1 + w.add_value)) AS price
FROM warehouse w
JOIN product p ON p.id = w.product_id
LEFT JOIN category c ON c.id = p.category_id
WHERE w.quantity > 0
ORDER BY p.name;

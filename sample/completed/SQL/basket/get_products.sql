SELECT
    p.product_id,
    p.product_name,
    p.price,
    c.category_name,
    p.in_stock
FROM products p
INNER JOIN categories c
    ON p.category_id = c.category_id
WHERE p.in_stock = TRUE
ORDER BY
    c.category_name,
    p.product_name

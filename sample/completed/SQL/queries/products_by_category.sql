SELECT
    p.product_id,
    p.product_name,
    p.price,
    c.category_name
FROM products p
INNER JOIN categories c
    ON p.category_id = c.category_id
WHERE
    p.category_id = %s
    AND p.in_stock = TRUE
ORDER BY p.product_name

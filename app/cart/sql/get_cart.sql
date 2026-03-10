SELECT ci.id,
       ci.product_id,
       p.sku,
       p.name,
       ci.quantity,
       ci.price_at_add,
       w.add_value,
       (ci.price_at_add * (1 + w.add_value)) AS price,
       w.quantity AS available
FROM cart_items ci
JOIN product p ON p.id = ci.product_id
LEFT JOIN category c ON c.id = p.category_id
JOIN warehouse w ON w.product_id = ci.product_id AND w.purchase_price = ci.price_at_add
WHERE ci.cart_id = %s
ORDER BY p.name;

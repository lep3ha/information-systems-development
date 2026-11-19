INSERT INTO order_items (
    order_id,
    product_id,
    quantity,
    price
)
VALUES (
    %s,
    %s,
    %s,
    %s
)

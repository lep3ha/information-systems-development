INSERT INTO orders (
    user_id,
    order_date
)
VALUES (
    %s,
    CURDATE()
)

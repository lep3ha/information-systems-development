INSERT INTO stock_balance (
    workpiece_id,
    price,
    quantity,
    updated_at
)
VALUES (
    %s,
    %s,
    %s,
    %s
)
ON CONFLICT (workpiece_id, price) DO UPDATE
SET
    quantity = stock_balance.quantity + EXCLUDED.quantity,
    updated_at = EXCLUDED.updated_at;

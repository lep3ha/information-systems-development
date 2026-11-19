INSERT INTO invoice (
    supplier_id,
    delivered_at,
    total
)
VALUES (
    %s,
    %s,
    %s
)
RETURNING id;

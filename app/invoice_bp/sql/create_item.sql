INSERT INTO invoice_item (
    invoice_id,
    workpiece_id,
    price,
    quantity
)
VALUES (
    %s,
    %s,
    %s,
    %s
);

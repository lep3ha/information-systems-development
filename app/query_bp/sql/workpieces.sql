SELECT w.id, w.name, t.name AS type, w.weight, w.material,
       b.price, b.quantity,
       b.updated_at AT TIME ZONE 'Europe/Moscow' AS updated_at
FROM workpiece AS w
JOIN workpiece_type AS t ON t.id = w.type_id
JOIN stock_balance AS b ON b.workpiece_id = w.id
WHERE w.type_id = %s;

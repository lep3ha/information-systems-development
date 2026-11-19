SELECT
    w.id,
    w.name,
    t.name AS type,
    w.weight,
    w.material
FROM workpiece AS w
JOIN workpiece_type AS t
    ON t.id = w.type_id
ORDER BY w.id;

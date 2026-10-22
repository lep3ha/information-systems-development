SELECT d.id,
       d.delivered_at AT TIME ZONE 'Europe/Moscow' AS delivered_at,
       s.company_name,
       COALESCE(SUM(di.price * di.quantity), 0) AS total
FROM delivery AS d
JOIN supplier AS s ON s.id = d.supplier_id
LEFT JOIN delivery_item AS di ON di.delivery_id = d.id
WHERE d.supplier_id = %s
  AND d.delivered_at >= (%s::date::timestamp AT TIME ZONE 'Europe/Moscow')
  AND d.delivered_at < ((%s::date + INTERVAL '1 day') AT TIME ZONE 'Europe/Moscow')
GROUP BY d.id, d.delivered_at, s.company_name;

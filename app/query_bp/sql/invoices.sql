SELECT i.id,
       i.delivered_at AT TIME ZONE 'Europe/Moscow' AS delivered_at,
       s.company_name,
       i.total
FROM invoice AS i
JOIN supplier AS s ON s.id = i.supplier_id
WHERE i.supplier_id = %s
  AND i.delivered_at >= (%s::date::timestamp AT TIME ZONE 'Europe/Moscow')
  AND i.delivered_at < ((%s::date + INTERVAL '1 day') AT TIME ZONE 'Europe/Moscow');

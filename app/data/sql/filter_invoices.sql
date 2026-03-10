SELECT 
    d.id,
    s.company_name as supplier_name,
    d.delivered_at as delivery_date,
    COALESCE(SUM(di.price * di.quantity), 0) as total_cost,
    COUNT(DISTINCT di.id) as item_count,
    COALESCE(SUM(di.quantity), 0) as total_quantity
FROM delivery d
INNER JOIN supplier s ON d.supplier_id = s.id
LEFT JOIN delivery_item di ON d.id = di.delivery_id
WHERE (d.supplier_id = {{ supplier_id }}::integer OR {{ supplier_id }} = 0)
  AND (d.delivered_at >= '{{ min_date }}'::date OR '{{ min_date }}' = '')
  AND (d.delivered_at <= '{{ max_date }}'::date OR '{{ max_date }}' = '')
GROUP BY d.id, s.id, s.company_name, d.delivered_at
HAVING (COALESCE(SUM(di.price * di.quantity), 0) >= {{ min_total }}::numeric OR {{ min_total }} = 0)
  AND (COALESCE(SUM(di.price * di.quantity), 0) <= {{ max_total }}::numeric OR {{ max_total }} = 0)
{% if sort_by == 'date_asc' %}
ORDER BY d.delivered_at ASC
{% elif sort_by == 'date_desc' %}
ORDER BY d.delivered_at DESC
{% elif sort_by == 'cost_asc' %}
ORDER BY COALESCE(SUM(di.price * di.quantity), 0) ASC
{% elif sort_by == 'cost_desc' %}
ORDER BY COALESCE(SUM(di.price * di.quantity), 0) DESC
{% elif sort_by == 'supplier_asc' %}
ORDER BY s.company_name ASC
{% elif sort_by == 'supplier_desc' %}
ORDER BY s.company_name DESC
{% else %}
ORDER BY d.delivered_at DESC
{% endif %};
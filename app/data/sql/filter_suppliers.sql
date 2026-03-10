SELECT 
    s.id,
    s.company_name AS name,
    s.city,
    s.contract_at AS contract_date,
    COUNT(DISTINCT d.id) as invoice_count,
    COALESCE(SUM(di.price * di.quantity), 0) as total_invoices
FROM supplier s
LEFT JOIN delivery d ON s.id = d.supplier_id
LEFT JOIN delivery_item di ON d.id = di.delivery_id
WHERE (s.city = '{{ city }}' OR '{{ city }}' = '')
  AND (s.contract_at >= '{{ min_date }}'::date OR '{{ min_date }}' = '')
  AND (s.contract_at <= '{{ max_date }}'::date OR '{{ max_date }}' = '')
GROUP BY s.id, s.company_name, s.city, s.contract_at
{% if sort_by == 'name_asc' %}
ORDER BY s.company_name ASC
{% elif sort_by == 'name_desc' %}
ORDER BY s.company_name DESC
{% elif sort_by == 'city_asc' %}
ORDER BY s.city ASC NULLS LAST
{% elif sort_by == 'city_desc' %}
ORDER BY s.city DESC NULLS LAST
{% elif sort_by == 'date_asc' %}
ORDER BY s.contract_at ASC
{% elif sort_by == 'date_desc' %}
ORDER BY s.contract_at DESC
{% elif sort_by == 'invoice_count_asc' %}
ORDER BY invoice_count ASC
{% elif sort_by == 'invoice_count_desc' %}
ORDER BY invoice_count DESC 
{% elif sort_by == 'total_invoices_asc' %}
ORDER BY total_invoices ASC
{% elif sort_by == 'total_invoices_desc' %}   
ORDER BY total_invoices DESC
{% else %}
ORDER BY s.company_name ASC
{% endif %};
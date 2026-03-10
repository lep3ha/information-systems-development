SELECT 
    p.id,
    p.sku as product_code,
    p.name,
    c.name as category,
    p.weight,
    wh.purchase_price as price,
    wh.quantity as quantity
FROM product p
JOIN warehouse wh ON p.id = wh.product_id
LEFT JOIN category c ON c.id = p.category_id
WHERE ('{{ category }}' = '' OR c.name = '{{ category }}')
  AND (wh.purchase_price >= {{ min_price }}::numeric OR {{ min_price }} = 0 OR wh.purchase_price IS NULL)
  AND (wh.purchase_price <= {{ max_price }}::numeric OR {{ max_price }} = 0 OR wh.purchase_price IS NULL)
{% if sort_by == 'name_asc' %}
ORDER BY p.name ASC
{% elif sort_by == 'name_desc' %}
ORDER BY p.name DESC
{% elif sort_by == 'price_asc' %}
ORDER BY wh.purchase_price ASC
{% elif sort_by == 'price_desc' %}
ORDER BY wh.purchase_price DESC
{% else %}
ORDER BY p.name ASC
{% endif %};
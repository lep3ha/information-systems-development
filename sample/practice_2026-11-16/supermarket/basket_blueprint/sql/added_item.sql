SELECT
    prod_name,
    prod_price
FROM product
WHERE prod_id = (%s)

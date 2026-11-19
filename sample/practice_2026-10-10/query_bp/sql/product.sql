SELECT
    prod_name,
    prod_measure,
    prod_price
FROM product
WHERE cat_id = %s

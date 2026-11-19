SELECT
    *
FROM sales_reports
WHERE
    report_month = %s
    AND report_year = %s
ORDER BY
    category_name,
    product_name;

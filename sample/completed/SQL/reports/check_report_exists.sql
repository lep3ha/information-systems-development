SELECT
    COUNT(*) AS count
FROM sales_reports
WHERE
    report_month = %s
    AND report_year = %s;

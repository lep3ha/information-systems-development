SELECT order_id, user_id, order_date, total_cost, items FROM sales_report_rows WHERE report_id = %s ORDER BY order_date;

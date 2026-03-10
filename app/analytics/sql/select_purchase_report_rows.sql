SELECT delivery_id, supplier_id, delivery_date, total_cost, items FROM purchase_report_rows WHERE report_id = %s ORDER BY delivery_date;

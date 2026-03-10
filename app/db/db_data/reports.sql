-- Reports schema: sales and purchase reports

-- Sales reports header
CREATE TABLE IF NOT EXISTS sales_reports (
	id SERIAL PRIMARY KEY,
	month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
	year INTEGER NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	created_by UUID
);

-- Sales report rows (one row per order included in the report)
CREATE TABLE IF NOT EXISTS sales_report_rows (
	id SERIAL PRIMARY KEY,
	report_id INTEGER NOT NULL REFERENCES sales_reports(id) ON DELETE CASCADE,
	order_id INTEGER NOT NULL,
	user_id UUID,
	order_date TIMESTAMP WITH TIME ZONE,
	total_cost DECIMAL(14,2),
	items JSONB -- aggregated items: [{product_id, quantity, price}, ...]
);

-- Purchase reports header
CREATE TABLE IF NOT EXISTS purchase_reports (
	id SERIAL PRIMARY KEY,
	month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
	year INTEGER NOT NULL,
	created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	created_by UUID
);

-- Purchase report rows (one row per delivery)
CREATE TABLE IF NOT EXISTS purchase_report_rows (
	id SERIAL PRIMARY KEY,
	report_id INTEGER NOT NULL REFERENCES purchase_reports(id) ON DELETE CASCADE,
	delivery_id INTEGER NOT NULL,
	supplier_id INTEGER,
	delivery_date TIMESTAMP WITH TIME ZONE,
	total_cost DECIMAL(14,2),
	items JSONB -- aggregated items for the delivery
);

-- Function to create sales report for given month/year
CREATE OR REPLACE FUNCTION fn_create_sales_report(p_month INTEGER, p_year INTEGER, p_creator UUID)
RETURNS INTEGER AS $$
DECLARE
	new_report_id INTEGER;
BEGIN
	-- Prevent duplicate reports
	IF EXISTS(SELECT 1 FROM sales_reports WHERE month = p_month AND year = p_year) THEN
		RAISE EXCEPTION 'Sales report for %/% already exists', p_month, p_year;
	END IF;

	INSERT INTO sales_reports (month, year, created_by)
	VALUES (p_month, p_year, p_creator)
	RETURNING id INTO new_report_id;

	-- Aggregate orders for the given month/year and insert rows
	INSERT INTO sales_report_rows (report_id, order_id, user_id, order_date, total_cost, items)
	SELECT
		new_report_id,
		o.id AS order_id,
		o.user_id,
		o.order_date,
		SUM(oi.quantity * oi.price_per_unit) AS total_cost,
		jsonb_agg(jsonb_build_object('product_id', oi.product_id, 'quantity', oi.quantity, 'price', oi.price_per_unit) ORDER BY oi.id) AS items
	FROM orders o
	JOIN order_items oi ON oi.order_id = o.id
	WHERE EXTRACT(MONTH FROM o.order_date) = p_month AND EXTRACT(YEAR FROM o.order_date) = p_year
	GROUP BY o.id, o.user_id, o.order_date;

	RETURN new_report_id;
END;
$$ LANGUAGE plpgsql;

-- Function to create purchase report for given month/year
CREATE OR REPLACE FUNCTION fn_create_purchase_report(p_month INTEGER, p_year INTEGER, p_creator UUID)
RETURNS INTEGER AS $$
DECLARE
	new_report_id INTEGER;
BEGIN
	IF EXISTS(SELECT 1 FROM purchase_reports WHERE month = p_month AND year = p_year) THEN
		RAISE EXCEPTION 'Purchase report for %/% already exists', p_month, p_year;
	END IF;

	INSERT INTO purchase_reports (month, year, created_by)
	VALUES (p_month, p_year, p_creator)
	RETURNING id INTO new_report_id;

	INSERT INTO purchase_report_rows (report_id, delivery_id, supplier_id, delivery_date, total_cost, items)
	SELECT
		new_report_id,
		d.id AS delivery_id,
		d.supplier_id,
		d.delivered_at AS delivery_date,
		SUM(di.price * di.quantity) AS total_cost,
		jsonb_agg(jsonb_build_object('product_id', di.product_id, 'quantity', di.quantity, 'price', di.price) ORDER BY di.id) AS items
	FROM delivery d
	JOIN delivery_item di ON di.delivery_id = d.id
	WHERE EXTRACT(MONTH FROM d.delivered_at) = p_month AND EXTRACT(YEAR FROM d.delivered_at) = p_year
	GROUP BY d.id, d.supplier_id, d.delivered_at;

	RETURN new_report_id;
END;
$$ LANGUAGE plpgsql;


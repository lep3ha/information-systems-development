BEGIN;

CREATE TABLE workpiece_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE workpiece (
    id SERIAL PRIMARY KEY,
    type_id INTEGER NOT NULL
        REFERENCES workpiece_type(id) ON DELETE RESTRICT,
    name VARCHAR(200) NOT NULL,
    weight NUMERIC(12, 3) NOT NULL CHECK (weight > 0),
    material VARCHAR(100) NOT NULL
);

CREATE TABLE stock_balance (
    workpiece_id INTEGER NOT NULL
        REFERENCES workpiece(id) ON DELETE RESTRICT,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    quantity INTEGER NOT NULL CHECK (quantity >= 0),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (workpiece_id, price)
);

CREATE TABLE supplier (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone VARCHAR(30),
    contract_date DATE NOT NULL
);

CREATE TABLE invoice (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL
        REFERENCES supplier(id) ON DELETE RESTRICT,
    delivered_at TIMESTAMP WITH TIME ZONE NOT NULL,
    total NUMERIC(14, 2) NOT NULL CHECK (total >= 0)
);

CREATE TABLE invoice_item (
    id SERIAL PRIMARY KEY,
    invoice_id INTEGER NOT NULL
        REFERENCES invoice(id) ON DELETE RESTRICT,
    workpiece_id INTEGER NOT NULL
        REFERENCES workpiece(id) ON DELETE RESTRICT,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

COMMIT;

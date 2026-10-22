BEGIN;

CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL
        REFERENCES category(id) ON DELETE RESTRICT,
    name VARCHAR(200) NOT NULL
);

CREATE TABLE supplier (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    phone VARCHAR(30)
);

CREATE TABLE delivery (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL
        REFERENCES supplier(id) ON DELETE RESTRICT,
    delivered_at TIMESTAMP WITH TIME ZONE NOT NULL
);

CREATE TABLE delivery_item (
    id SERIAL PRIMARY KEY,
    delivery_id INTEGER NOT NULL
        REFERENCES delivery(id) ON DELETE RESTRICT,
    product_id INTEGER NOT NULL
        REFERENCES product(id) ON DELETE RESTRICT,
    price NUMERIC(12, 2) NOT NULL CHECK (price >= 0),
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

COMMIT;

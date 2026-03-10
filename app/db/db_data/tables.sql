
-- Таблица пользователей
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(100) DEFAULT 'none',
    second_name VARCHAR(100) DEFAULT 'none',
    password_hash VARCHAR(255) NOT NULL, -- храним хеш пароля, не сам пароль
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Таблица разрешений пользователей
CREATE TABLE user_permission (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    permission VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL,
    CONSTRAINT permission_user_fk
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    CHECK (permission IN ('catalog', 'suppliers', 'invoices', 'reports', 'monitoring')),
    CHECK (role IN ('creator', 'editor', 'viewer')),
    UNIQUE(user_id, permission, role)
);

-- Таблица поставщиков
CREATE TABLE supplier (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    contract_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Таблица заготовок
-- Категории продуктов
CREATE TABLE IF NOT EXISTS category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Таблица продуктов (магазин продуктов)
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES category(id) ON DELETE RESTRICT,
    name VARCHAR(200) NOT NULL,
    weight DECIMAL(10, 3),
    sku UUID UNIQUE DEFAULT gen_random_uuid()
);

-- Таблица накладных поставки
CREATE TABLE delivery (
    id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    delivered_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT delivery_suppliers_fk
        FOREIGN KEY (supplier_id)
        REFERENCES supplier(id)
        ON DELETE RESTRICT
);


-- Таблица поставляемых заготовок
CREATE TABLE delivery_item (
    id SERIAL PRIMARY KEY,
    delivery_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL REFERENCES product(id) ON DELETE RESTRICT,
    price DECIMAL(12, 2) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),

    UNIQUE(id, product_id),
    CONSTRAINT delivery_item_delivery_fk
        FOREIGN KEY (delivery_id)
        REFERENCES delivery(id)
        ON DELETE CASCADE
);

-- Таблица склада
CREATE TABLE warehouse (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    purchase_price DECIMAL(12, 2) NOT NULL, -- цена покупки продукта
    add_value DECIMAL(12, 4) NOT NULL, -- процент добавочной стоимости
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0), -- количество на складе
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT product_warehouse_fk
        FOREIGN KEY (product_id)
        REFERENCES product(id)
        ON DELETE RESTRICT,
    UNIQUE(product_id, purchase_price) -- чтобы не дублировать одинаковые продукты с одной ценой закупки
);


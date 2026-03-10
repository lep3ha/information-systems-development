-- 1. Таблица корзины (сессии покупок)
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE
);

-- 2. Таблица элементов корзины
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_at_add DECIMAL(12, 2) NOT NULL, -- цена на момент добавления
    UNIQUE(cart_id, product_id), -- товар может быть только один раз в корзине
    CONSTRAINT cart_items_warehouse_fk
        FOREIGN KEY (product_id, price_at_add)
        REFERENCES warehouse(product_id, purchase_price)
        ON DELETE RESTRICT,
    CONSTRAINT cart_items_cart_fk
        FOREIGN KEY (cart_id)
        REFERENCES carts(id)
        ON DELETE CASCADE
);

-- 3. Таблица заказов
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    order_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT orders_user_fk
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE RESTRICT
);

-- 4. Таблица элементов заказа
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price_per_unit DECIMAL(12, 2) NOT NULL, -- цена продажи на момент заказа
    UNIQUE(order_id, product_id),
    CONSTRAINT order_items_warehouse_fk
        FOREIGN KEY (product_id, price_per_unit)
        REFERENCES warehouse(product_id, purchase_price)
        ON DELETE RESTRICT,
    CONSTRAINT order_order_items_id_fk
        FOREIGN KEY (order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE
);
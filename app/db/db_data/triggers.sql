-- Триггеры для автоматического заполнения и поддержания склада
-- Синхронизируют таблицу `warehouse` при изменениях в `delivery_item`

CREATE OR REPLACE FUNCTION fn_delivery_item_after_insert()
RETURNS trigger AS $$
BEGIN
        -- Попытка обновить существующую запись склада
        UPDATE warehouse
        SET quantity = quantity + NEW.quantity,
                last_updated = CURRENT_TIMESTAMP
        WHERE product_id = NEW.product_id
            AND purchase_price = NEW.price;

    -- Если запись не обновилась (нет совпадения), вставить новую
    IF NOT FOUND THEN
        INSERT INTO warehouse (product_id, purchase_price, add_value, quantity, last_updated)
        VALUES (NEW.product_id, NEW.price, 0.2000, NEW.quantity, CURRENT_TIMESTAMP);
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_delivery_item_after_delete()
RETURNS trigger AS $$
DECLARE
    remaining INTEGER;
BEGIN
        -- Уменьшаем количество на складе на величину удаляемой позиции
        UPDATE warehouse
        SET quantity = quantity - OLD.quantity,
                last_updated = CURRENT_TIMESTAMP
        WHERE product_id = OLD.product_id
            AND purchase_price = OLD.price;

    -- Удаляем записи с нулевым или отрицательным количеством
        DELETE FROM warehouse
        WHERE product_id = OLD.product_id
            AND purchase_price = OLD.price
            AND quantity <= 0;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_delivery_item_after_update()
RETURNS trigger AS $$
DECLARE
    delta INTEGER;
BEGIN
        -- Если цена или продукт изменились, перенести количество со старой записи на новую
        IF (OLD.price IS DISTINCT FROM NEW.price) OR (OLD.product_id IS DISTINCT FROM NEW.product_id) THEN
                -- Вычитаем старое количество из старой складской записи
                UPDATE warehouse
                SET quantity = quantity - OLD.quantity,
                        last_updated = CURRENT_TIMESTAMP
                WHERE product_id = OLD.product_id
                    AND purchase_price = OLD.price;

                -- Удаляем записи с нулем или отрицанием
                DELETE FROM warehouse
                WHERE product_id = OLD.product_id
                    AND purchase_price = OLD.price
                    AND quantity <= 0;

                -- Добавляем или обновляем новую складскую запись с новым price/product
                UPDATE warehouse
                SET quantity = quantity + NEW.quantity,
                        last_updated = CURRENT_TIMESTAMP
                WHERE product_id = NEW.product_id
                    AND purchase_price = NEW.price;

                IF NOT FOUND THEN
                        INSERT INTO warehouse (product_id, purchase_price, add_value, quantity, last_updated)
                        VALUES (NEW.product_id, NEW.price, 0.2000, NEW.quantity, CURRENT_TIMESTAMP);
                END IF;

    ELSE
        -- Если изменилась только величина quantity, корректируем дельту
        delta := NEW.quantity - OLD.quantity;
        IF delta <> 0 THEN
            UPDATE warehouse
            SET quantity = quantity + delta,
                last_updated = CURRENT_TIMESTAMP
            WHERE product_id = NEW.product_id
              AND purchase_price = NEW.price;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Триггеры, привязанные к событиям в delivery_item
CREATE TRIGGER trg_delivery_item_after_insert
AFTER INSERT ON delivery_item
FOR EACH ROW
EXECUTE FUNCTION fn_delivery_item_after_insert();

CREATE TRIGGER trg_delivery_item_after_delete
AFTER DELETE ON delivery_item
FOR EACH ROW
EXECUTE FUNCTION fn_delivery_item_after_delete();

CREATE TRIGGER trg_delivery_item_after_update
AFTER UPDATE ON delivery_item
FOR EACH ROW
EXECUTE FUNCTION fn_delivery_item_after_update();

-- Триггеры для уменьшения количества заготовок на складе при оформлении заказа

CREATE OR REPLACE FUNCTION fn_order_items_after_insert()
RETURNS trigger AS $$
BEGIN
        -- Уменьшаем количество на складе на величину добавленного в заказ товара
        UPDATE warehouse
        SET quantity = quantity - NEW.quantity,
                last_updated = CURRENT_TIMESTAMP
        WHERE product_id = NEW.product_id
            AND purchase_price = NEW.price_per_unit;

        -- Если количество стало отрицательным, возвращаем ошибку
        IF (SELECT quantity FROM warehouse 
                WHERE product_id = NEW.product_id 
                    AND purchase_price = NEW.price_per_unit) < 0 THEN
                RAISE EXCEPTION 'Недостаточно товара на складе. Заказ не может быть оформлен.';
        END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_order_items_after_delete()
RETURNS trigger AS $$
BEGIN
        -- Возвращаем товар на склад при удалении заказа
        UPDATE warehouse
        SET quantity = quantity + OLD.quantity,
                last_updated = CURRENT_TIMESTAMP
        WHERE product_id = OLD.product_id
            AND purchase_price = OLD.price_per_unit;

    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

-- Триггеры, привязанные к событиям в order_items
CREATE TRIGGER trg_order_items_after_insert
AFTER INSERT ON order_items
FOR EACH ROW
EXECUTE FUNCTION fn_order_items_after_insert();

CREATE TRIGGER trg_order_items_after_delete
AFTER DELETE ON order_items
FOR EACH ROW
EXECUTE FUNCTION fn_order_items_after_delete();

-- Конец triggers.sql

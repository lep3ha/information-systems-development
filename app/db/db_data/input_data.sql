BEGIN;

INSERT INTO workpiece_type (name) VALUES
    ('Прокат'),
    ('Поковки'),
    ('Отливки'),
    ('Штамповки');

INSERT INTO workpiece (type_id, name, weight, material) VALUES
    (1, 'Круг стальной Ø20 мм', 2.500, 'Сталь 45'),
    (1, 'Лист стальной 2 мм', 7.850, 'Сталь Ст3'),
    (2, 'Поковка вала', 4.200, 'Сталь 40Х'),
    (2, 'Поковка фланца', 1.800, 'Сталь 20'),
    (3, 'Отливка корпуса', 6.000, 'Чугун СЧ20'),
    (3, 'Отливка крышки', 1.200, 'Алюминий АК12');

INSERT INTO supplier (company_name, city, phone, contract_date) VALUES
    ('МеталлСнаб', 'Москва', '+7-495-111-11-11', '2020-02-10'),
    ('Невский кузнечный завод', 'Санкт-Петербург', '+7-812-222-22-22', '2020-03-01'),
    ('Литейный двор', 'Москва', NULL, '2020-02-20'),
    ('Заготовки Поволжья', 'Казань', '+7-843-333-33-33', '2020-07-15');

INSERT INTO invoice (supplier_id, delivered_at, total) VALUES
    (1, '2026-03-01 00:00:00+03', 17000.00),
    (1, '2026-03-15 12:00:00+03', 18100.00),
    (1, '2026-03-31 23:59:59.999999+03', 6000.00),
    (1, '2026-04-01 00:00:00+03', 1000.00),
    (2, '2026-03-15 10:00:00+03', 13000.00),
    (3, '2026-02-28 23:59:59.999999+03', 11100.00);

INSERT INTO invoice_item (invoice_id, workpiece_id, price, quantity) VALUES
    (1, 1, 900.00, 10),
    (1, 2, 2000.00, 4),
    (2, 1, 950.00, 8),
    (2, 2, 2100.00, 5),
    (3, 1, 1000.00, 6),
    (4, 1, 1000.00, 1),
    (5, 3, 500.00, 20),
    (5, 4, 300.00, 10),
    (6, 5, 1500.00, 5),
    (6, 6, 1200.00, 3);

-- Начальные остатки рассчитаны по всем строкам накладных.
-- Каждая цена одной заготовки учитывается отдельно.
INSERT INTO stock_balance (workpiece_id, price, quantity, updated_at)
SELECT item.workpiece_id, item.price, SUM(item.quantity), MAX(invoice.delivered_at)
FROM invoice_item AS item
JOIN invoice ON invoice.id = item.invoice_id
GROUP BY item.workpiece_id, item.price;

COMMIT;

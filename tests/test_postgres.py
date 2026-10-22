import json
import os
from pathlib import Path
import unittest
from uuid import uuid4

import psycopg2
from psycopg2 import sql

from app.db.context_manager import DBContextManager
from app.main_menu import app


@unittest.skipUnless(os.environ.get("LAB1_TEST_DB_CONFIG"), "Не задан LAB1_TEST_DB_CONFIG для PostgreSQL")
class PostgreSQLTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = json.loads(Path(os.environ["LAB1_TEST_DB_CONFIG"]).read_text(encoding="utf-8"))
        cls.connection = psycopg2.connect(**config)
        cls.addClassCleanup(cls.connection.close)
        cls.connection.autocommit = True
        cls.schema = "lab1_test_" + uuid4().hex
        with cls.connection.cursor() as cursor:
            cursor.execute(sql.SQL("CREATE SCHEMA {}").format(sql.Identifier(cls.schema)))
        cls.addClassCleanup(cls.drop_schema)
        cls.db_config = dict(config)
        cls.db_config["options"] = config.get("options", "") + f" -c search_path={cls.schema}"
        root = Path(__file__).resolve().parents[1]
        with cls.connection.cursor() as cursor:
            cursor.execute(sql.SQL("SET search_path TO {}").format(sql.Identifier(cls.schema)))
            for filename in ("tables.sql", "input_data.sql"):
                cursor.execute((root / "app/db/db_data" / filename).read_text(encoding="utf-8"))

    @classmethod
    def drop_schema(cls):
        with cls.connection.cursor() as cursor:
            cursor.execute("ROLLBACK")
            cursor.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(cls.schema)))

    def setUp(self):
        self.previous_config = app.config.copy()
        app.config.update(TESTING=True, db_config=self.db_config)
        self.client = app.test_client()

    def tearDown(self):
        app.config.clear()
        app.config.update(self.previous_config)

    def test_products_and_empty_category(self):
        response = self.client.post("/query/products", data={"category_id": "1"})
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Молоко 1 л", html)
        self.assertIn("Сыр 200 г", html)
        self.assertNotIn("Хлеб ржаной", html)
        response = self.client.post("/query/products", data={"category_id": "4"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ничего не найдено", response.get_data(as_text=True))

    def test_suppliers_and_sql_parameter_binding(self):
        response = self.client.post("/query/suppliers", data={"city": "Москва"})
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        self.assertIn("Молочный двор", html)
        self.assertIn("Фруктовый сад", html)
        self.assertNotIn("Пекарня Нева", html)
        response = self.client.post("/query/suppliers", data={"city": "Москва' OR 1=1 --"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ничего не найдено", response.get_data(as_text=True))

    def test_delivery_totals_and_inclusive_moscow_period(self):
        response = self.client.post("/query/deliveries", data={
            "supplier_id": "1", "start_date": "2026-10-01", "end_date": "2026-10-31",
        })
        self.assertEqual(response.status_code, 200)
        html = response.get_data(as_text=True)
        for expected in ("1700.00", "1810.00", "600.00", "2026-10-01 00:00:00", "2026-10-31 23:59:59.999999"):
            self.assertIn(expected, html)
        self.assertNotIn("2026-11-01", html)
        self.assertNotIn("Пекарня Нева", html)
        response = self.client.post("/query/deliveries", data={
            "supplier_id": "1", "start_date": "2026-10-31", "end_date": "2026-10-31",
        })
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("600.00", html)
        self.assertNotIn("1700.00", html)

    def test_database_constraints(self):
        cases = (
            ("INSERT INTO category (name) VALUES (%s)", ("Молочные продукты",)),
            ("INSERT INTO product (category_id, name) VALUES (%s, %s)", (999999, "Нет категории")),
            ("INSERT INTO delivery_item (delivery_id, product_id, price, quantity) VALUES (%s, %s, %s, %s)", (1, 1, -1, 1)),
            ("INSERT INTO delivery_item (delivery_id, product_id, price, quantity) VALUES (%s, %s, %s, %s)", (1, 1, 1, 0)),
            ("DELETE FROM delivery WHERE id = %s", (1,)),
            ("DELETE FROM product WHERE id = %s", (1,)),
        )
        for statement, params in cases:
            with self.subTest(statement=statement, params=params):
                with self.assertRaises(psycopg2.IntegrityError):
                    with DBContextManager(self.db_config) as cursor:
                        cursor.execute(statement, params)

    def test_commit_rollback_and_connection_release(self):
        committed = DBContextManager(self.db_config)
        with committed as cursor:
            cursor.execute("INSERT INTO category (name) VALUES (%s)", ("Проверка фиксации",))
        self.assertTrue(committed.connection.closed)
        self.assertTrue(committed.cursor.closed)

        rolled_back = DBContextManager(self.db_config)
        with self.assertRaises(RuntimeError):
            with rolled_back as cursor:
                cursor.execute("INSERT INTO category (name) VALUES (%s)", ("Проверка отката",))
                raise RuntimeError("Проверка отката")
        self.assertTrue(rolled_back.connection.closed)
        self.assertTrue(rolled_back.cursor.closed)
        with DBContextManager(self.db_config) as cursor:
            cursor.execute("SELECT name FROM category WHERE name IN (%s, %s)", ("Проверка фиксации", "Проверка отката"))
            self.assertEqual(cursor.fetchall(), [("Проверка фиксации",)])


if __name__ == "__main__":
    unittest.main()

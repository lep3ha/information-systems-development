import unittest
from datetime import date
from decimal import Decimal
from unittest.mock import Mock, patch

from psycopg2 import OperationalError

from app.db.context_manager import DBContextManager
from app.main_menu import app


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.previous_config = app.config.copy()
        app.config.update(TESTING=True, db_config={"dbname": "test"})
        self.client = app.test_client()

    def tearDown(self):
        app.config.clear()
        app.config.update(self.previous_config)

    def test_navigation_and_forms(self):
        for path, text in (
            ("/", "Главное меню"),
            ("/exit", "До свидания"),
            ("/query/", "Меню запросов"),
            ("/query/products", "Код категории"),
            ("/query/suppliers", "Город"),
            ("/query/deliveries", "Начальная дата"),
        ):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(text, response.get_data(as_text=True))
        self.assertEqual(self.client.get("/query/unknown").status_code, 404)

    @patch("app.query_bp.model_route.select_dict")
    def test_invalid_parameters_do_not_reach_database(self, select):
        cases = [
            ("products", {}),
            ("products", {"category_id": "0"}),
            ("products", {"category_id": "1.5"}),
            ("products", {"category_id": "2147483648"}),
            ("suppliers", {"city": "   "}),
            ("suppliers", {"city": "x" * 101}),
            ("suppliers", {"city": "Москва\x00"}),
            ("deliveries", {"supplier_id": "1", "start_date": "2026-02-30", "end_date": "2026-03-01"}),
            ("deliveries", {"supplier_id": "1", "start_date": "2026-11-01", "end_date": "2026-10-01"}),
            ("deliveries", {"supplier_id": "1", "start_date": "2026-10-01"}),
        ]
        for query, values in cases:
            with self.subTest(query=query, values=values):
                response = self.client.post(f"/query/{query}", data=values)
                self.assertEqual(response.status_code, 400)
                self.assertIn('role="alert"', response.get_data(as_text=True))
        select.assert_not_called()

    @patch("app.query_bp.model_route.select_dict", return_value=[])
    def test_empty_result_is_success(self, select):
        response = self.client.post("/query/products", data={"category_id": "4"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ничего не найдено", response.get_data(as_text=True))

    @patch("app.query_bp.model_route.select_dict", return_value=[])
    def test_city_is_passed_as_a_parameter(self, select):
        city = "Москва' OR 1=1 --"
        self.client.post("/query/suppliers", data={"city": city})
        sql, params = select.call_args.args
        self.assertNotIn(city, sql)
        self.assertEqual(params, {"city": city})

    @patch("app.query_bp.model_route.select_dict", return_value=[])
    def test_period_parameters_are_validated_dates(self, select):
        response = self.client.post("/query/deliveries", data={
            "supplier_id": "1", "start_date": "2026-10-01", "end_date": "2026-10-31",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(select.call_args.args[1], {
            "supplier_id": 1, "start_date": date(2026, 10, 1), "end_date": date(2026, 10, 31),
        })

    @patch("app.query_bp.model_route.select_dict")
    def test_results_are_rendered_and_escaped(self, select):
        cases = (
            ("products", {"category_id": "1"}, [{"id": 1, "name": "<script>milk</script>", "category": "Молочные"}], "&lt;script&gt;milk&lt;/script&gt;"),
            ("suppliers", {"city": "Москва"}, [{"company_name": "Фрукты", "city": "Москва", "phone": None}], "Фрукты"),
            ("deliveries", {"supplier_id": "1", "start_date": "2026-10-01", "end_date": "2026-10-31"}, [{"id": 1, "delivered_at": "2026-10-01 00:00:00", "company_name": "Молочный двор", "total": Decimal("1700.00")}], "1700.00"),
        )
        for query, values, rows, text in cases:
            with self.subTest(query=query):
                select.return_value = rows
                response = self.client.post(f"/query/{query}", data=values)
                self.assertEqual(response.status_code, 200)
                html = response.get_data(as_text=True)
                self.assertIn(text, html)
                self.assertNotIn("<script>", html)
                self.assertIn("Повторить запрос", html)

    @patch("app.query_bp.model_route.select_dict", side_effect=OperationalError("PRIVATE DATABASE DETAILS"))
    def test_database_failure_keeps_values_and_hides_details(self, select):
        with self.assertLogs(app.logger, level="ERROR") as logs:
            response = self.client.post("/query/suppliers", data={"city": "Москва"})
        html = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 503)
        self.assertIn('value="Москва"', html)
        self.assertNotIn("PRIVATE DATABASE DETAILS", html)
        self.assertIn("PRIVATE DATABASE DETAILS", "\n".join(logs.output))

    @patch("app.query_bp.model_route.select_dict")
    def test_missing_database_config_is_service_unavailable(self, select):
        app.config.pop("db_config")
        with self.assertLogs(app.logger, level="ERROR"):
            response = self.client.post("/query/products", data={"category_id": "1"})
        self.assertEqual(response.status_code, 503)
        select.assert_not_called()


class TransactionTests(unittest.TestCase):
    def setUp(self):
        self.connection = Mock()
        self.cursor = self.connection.cursor.return_value
        connect = patch("app.db.context_manager.connect", return_value=self.connection)
        self.connect = connect.start()
        self.addCleanup(connect.stop)

    def test_success_commits_and_releases_resources(self):
        with DBContextManager({"dbname": "test"}) as cursor:
            cursor.execute("SELECT 1")
        self.connect.assert_called_once_with(dbname="test")
        self.connection.commit.assert_called_once()
        self.connection.rollback.assert_not_called()
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_query_failure_rolls_back_and_propagates(self):
        self.cursor.execute.side_effect = OperationalError("query failed")
        with self.assertRaises(OperationalError):
            with DBContextManager({}) as cursor:
                cursor.execute("SELECT 1")
        self.connection.rollback.assert_called_once()
        self.connection.commit.assert_not_called()
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_commit_failure_rolls_back_and_releases_resources(self):
        self.connection.commit.side_effect = OperationalError("commit failed")
        with self.assertRaises(OperationalError):
            with DBContextManager({}):
                pass
        self.connection.rollback.assert_called_once()
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_cursor_creation_failure_releases_connection(self):
        self.connection.cursor.side_effect = OperationalError("cursor failed")
        with self.assertRaises(OperationalError):
            with DBContextManager({}):
                self.fail("Context body must not run")
        self.connection.rollback.assert_called_once()
        self.connection.close.assert_called_once()

    def test_rollback_failure_still_releases_resources(self):
        self.connection.rollback.side_effect = OperationalError("rollback failed")
        with self.assertRaises(OperationalError):
            with DBContextManager({}):
                raise ValueError("query failed")
        self.cursor.close.assert_called_once()
        self.connection.close.assert_called_once()

    def test_cursor_close_failure_still_closes_connection(self):
        self.cursor.close.side_effect = OperationalError("close failed")
        with self.assertRaises(OperationalError):
            with DBContextManager({}):
                pass
        self.connection.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()

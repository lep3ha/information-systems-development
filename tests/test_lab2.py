import unittest
from unittest.mock import patch

from psycopg2 import OperationalError
from werkzeug.security import generate_password_hash

from app.main_menu import app


class AuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = {
            "user_id": 1, "user_group": "admin",
            "password_hash": generate_password_hash("admin"),
        }

    def setUp(self):
        self.previous_config = app.config.copy()
        app.config.update(TESTING=True, SECRET_KEY="lab2-test", db_config={"dbname": "test"})
        self.client = app.test_client()

    def tearDown(self):
        app.config.clear()
        app.config.update(self.previous_config)

    def test_anonymous_requests_redirect_before_query_execution(self):
        with patch("app.query_bp.model_route.select_list") as select:
            for path in ("/", "/query/", "/query/workpieces", "/query/suppliers", "/query/invoices"):
                with self.subTest(path=path):
                    response = self.client.get(path)
                    self.assertEqual(response.status_code, 302)
                    self.assertEqual(response.location, "/auth/")
            self.assertEqual(self.client.post("/query/workpieces", data={"type_id": "1"}).location, "/auth/")
            select.assert_not_called()

    def test_login_form_and_required_fields(self):
        self.assertIn('type="password"', self.client.get("/auth/").get_data(as_text=True))
        with patch("app.auth_bp.model_route.select_list") as select:
            for data in ({}, {"login": "admin"}, {"password": "admin"}, {"login": "a\x00", "password": "admin"}):
                self.assertEqual(self.client.post("/auth/", data=data).status_code, 400)
            select.assert_not_called()

    @patch("app.auth_bp.model_route.select_list")
    def test_success_creates_session_and_redirects_to_menu(self, select):
        select.return_value = [self.user]
        with self.client.session_transaction() as session:
            session["old_value"] = "remove"
        response = self.client.post("/auth/", data={"login": "admin", "password": "admin"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/")
        with self.client.session_transaction() as session:
            self.assertEqual(dict(session), {"user_id": 1, "user_group": "admin", "_permanent": True})
        self.assertEqual(self.client.get("/").status_code, 200)
        for path in ("/query/", "/query/workpieces", "/query/suppliers", "/query/invoices"):
            self.assertEqual(self.client.get(path).status_code, 200)

    @patch("app.auth_bp.model_route.select_list")
    def test_wrong_credentials_and_unknown_login(self, select):
        for rows in ([], [self.user]):
            select.return_value = rows
            response = self.client.post("/auth/", data={"login": "<admin>", "password": "private-wrong-password"})
            self.assertEqual(response.status_code, 401)
            html = response.get_data(as_text=True)
            self.assertIn("Неверный логин или пароль", html)
            self.assertIn("&lt;admin&gt;", html)
            self.assertNotIn("private-wrong-password", html)
            with self.client.session_transaction() as session:
                self.assertNotIn("user_group", session)

    @patch("app.auth_bp.model_route.select_list", return_value=[])
    def test_sql_parameters_ignore_form_field_order_and_extra_fields(self, select):
        login = "admin' OR 1=1 --"
        self.client.post("/auth/", data={"password": "admin", "user_group": "admin", "login": login})
        statement, params = select.call_args.args
        self.assertNotIn(login, statement)
        self.assertEqual(params, {"login": login})

    @patch("app.auth_bp.model_route.select_list", side_effect=OperationalError("PRIVATE DETAILS"))
    def test_database_failure(self, select):
        with self.assertLogs(app.logger, level="ERROR"):
            response = self.client.post("/auth/", data={"login": "admin", "password": "admin"})
        self.assertEqual(response.status_code, 503)
        self.assertNotIn("PRIVATE DETAILS", response.get_data(as_text=True))
        with self.client.session_transaction() as session:
            self.assertNotIn("user_group", session)

    @patch("app.auth_bp.model_route.select_list")
    def test_missing_database_config(self, select):
        app.config.pop("db_config")
        with self.assertLogs(app.logger, level="ERROR"):
            response = self.client.post("/auth/", data={"login": "admin", "password": "admin"})
        self.assertEqual(response.status_code, 503)
        select.assert_not_called()

    def test_storekeeper_and_unknown_group_cannot_access_queries(self):
        with patch("app.query_bp.model_route.select_list") as select:
            for group in ("storekeeper", "unknown"):
                with self.client.session_transaction() as session:
                    session["user_id"] = 2
                    session["user_group"] = group
                self.assertEqual(self.client.get("/").status_code, 200)
                for path in ("/query/", "/query/workpieces", "/query/suppliers", "/query/invoices"):
                    with self.subTest(group=group, path=path):
                        self.assertEqual(self.client.get(path).status_code, 403)
                        self.assertEqual(self.client.post(path, data={"type_id": "1"}).status_code, 403 if path != "/query/" else 405)
            select.assert_not_called()

    def test_exit_clears_session(self):
        with self.client.session_transaction() as session:
            session["user_id"] = 1
            session["user_group"] = "admin"
        self.assertEqual(self.client.get("/exit").status_code, 200)
        with self.client.session_transaction() as session:
            self.assertEqual(dict(session), {})
        self.assertEqual(self.client.get("/").location, "/auth/")
        self.assertEqual(self.client.get("/query/").location, "/auth/")

    def test_tampered_cookie_does_not_authorize(self):
        self.client.set_cookie("session", "forged-admin-session")
        self.assertEqual(self.client.get("/").location, "/auth/")


if __name__ == "__main__":
    unittest.main()

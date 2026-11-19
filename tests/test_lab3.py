from decimal import Decimal
import unittest
from unittest.mock import patch

from app.main_menu import app


class InvoiceTests(unittest.TestCase):
    def setUp(self):
        self.previous_config = app.config.copy()
        app.config.update(TESTING=True, SECRET_KEY="lab3-test", db_config={})
        self.addCleanup(self.restore_config)
        self.client = app.test_client()
        self.login("storekeeper")
        self.catalog = patch("app.invoice_bp.route.catalog", return_value=(
            [{"id": 1, "company_name": "Поставщик"}],
            [{"id": 1, "name": "Заготовка", "type": "Прокат", "weight": Decimal("1.5"), "material": "Сталь"}],
        ))
        self.catalog.start()
        self.addCleanup(self.catalog.stop)

    def restore_config(self):
        app.config.clear()
        app.config.update(self.previous_config)

    def login(self, group):
        with self.client.session_transaction() as session:
            session.clear()
            if group:
                session.update(user_id=1, user_group=group)

    def post(self, **values):
        data = {"supplier_id": "1", "delivered_at": "2026-11-19"}
        data.update(values)
        return self.client.post("/invoice/", data=data)

    def add(self, price="10.20", quantity="2"):
        return self.post(workpiece_id="1", price_1=price, quantity_1=quantity)

    def test_roles(self):
        for group, status in ((None, 302), ("unknown", 403), ("admin", 200), ("storekeeper", 200)):
            self.login(group)
            self.assertEqual(self.client.get("/invoice/").status_code, status)
            self.assertEqual(self.post(action="clear").status_code, 302 if status == 200 else status)

    def test_add_separate_lines_prices_remove_clear_and_total(self):
        for price in ("10.20", "10.20", "20.00"):
            self.assertEqual(self.add(price).status_code, 302)
        with self.client.session_transaction() as session:
            self.assertEqual(len(session["invoice_draft"]["lines"]), 3)
        html = self.client.get("/invoice/").get_data(as_text=True)
        self.assertIn("80.80", html)
        self.assertEqual(self.post(action="remove:1").status_code, 302)
        with self.client.session_transaction() as session:
            self.assertEqual(len(session["invoice_draft"]["lines"]), 2)
        self.assertEqual(self.post(action="clear").status_code, 302)
        with self.client.session_transaction() as session:
            self.assertEqual(session["invoice_draft"]["lines"], [])

    def test_success_clears_draft(self):
        self.add()
        with patch("app.invoice_bp.route.save_invoice", return_value=42) as save:
            response = self.post(action="accept")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Накладная № 42", response.get_data(as_text=True))
        self.assertEqual(save.call_args.args[1]["lines"][0]["price"], "10.20")
        with self.client.session_transaction() as session:
            self.assertNotIn("invoice_draft", session)

    def test_failure_keeps_draft(self):
        from psycopg2 import OperationalError
        self.add()
        with patch("app.invoice_bp.route.save_invoice", side_effect=OperationalError("test")):
            response = self.post(action="accept")
        self.assertEqual(response.status_code, 503)
        with self.client.session_transaction() as session:
            self.assertEqual(len(session["invoice_draft"]["lines"]), 1)

    def test_required_fields_and_empty_invoice(self):
        for price, quantity in (("", "1"), ("1", "")):
            self.assertEqual(self.add(price, quantity).status_code, 400)
        self.assertEqual(self.post(action="accept").status_code, 400)
        with self.client.session_transaction() as session:
            self.assertEqual(session["invoice_draft"]["lines"], [])


if __name__ == "__main__":
    unittest.main()

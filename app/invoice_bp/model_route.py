from datetime import date, datetime, time
from decimal import Decimal
from zoneinfo import ZoneInfo

from flask import current_app

from app.db.context_manager import DBContextManager
from app.db.select import select_list


def catalog(provider):
    return (
        select_list(provider.get("suppliers.sql"), {}),
        select_list(provider.get("workpieces.sql"), {}),
    )


def invoice_line(values):
    return {
        "workpiece_id": int(values["workpiece_id"]),
        "price": str(Decimal(values["price"])),
        "quantity": int(values["quantity"]),
    }


def invoice_header(draft):
    if not draft["supplier_id"] or not draft["delivered_at"]:
        raise ValueError("Выберите поставщика и дату поставки.")
    supplier_id = int(draft["supplier_id"])
    delivered = date.fromisoformat(draft["delivered_at"])
    return supplier_id, datetime.combine(delivered, time.min, ZoneInfo("Europe/Moscow"))


def line_total(line):
    return Decimal(line["price"]) * line["quantity"]


def save_invoice(provider, draft):
    supplier_id, delivered_at = invoice_header(draft)
    lines = draft["lines"]
    if not lines:
        raise ValueError("Добавьте хотя бы одну заготовку.")
    total = sum((line_total(line) for line in lines), Decimal("0.00"))

    with DBContextManager(current_app.config["db_config"]) as cursor:
        cursor.execute(provider.get("create_invoice.sql"), (supplier_id, delivered_at, total))
        invoice_id = cursor.fetchone()[0]
        for line in lines:
            price = Decimal(line["price"])
            cursor.execute(provider.get("create_item.sql"),
                           (invoice_id, line["workpiece_id"], price, line["quantity"]))
            cursor.execute(provider.get("update_stock.sql"),
                           (line["workpiece_id"], price, line["quantity"], delivered_at))
    return invoice_id

from datetime import datetime
from decimal import Decimal
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Blueprint, current_app, redirect, render_template, request, session, url_for
from psycopg2 import Error

from app.access import group_required
from app.db.sql_provider import SQLProvider
from app.invoice_bp.model_route import catalog, invoice_line, line_total, save_invoice


blueprint_invoice = Blueprint("invoice_bp", __name__, template_folder="templates")
provider = SQLProvider(Path(__file__).parent / "sql")


@blueprint_invoice.route("/", methods=["GET", "POST"])
@group_required
def invoice_index():
    draft = session.get("invoice_draft", {
        "supplier_id": "", "delivered_at": datetime.now(ZoneInfo("Europe/Moscow")).date().isoformat(),
        "lines": [],
    })
    error = ""
    status_code = 200
    suppliers, workpieces = [], []
    if request.method == "POST":
        draft["supplier_id"] = request.form.get("supplier_id", "")
        draft["delivered_at"] = request.form.get("delivered_at", "")
        session["invoice_draft"] = draft
    try:
        suppliers, workpieces = catalog(provider)
        if request.method == "POST":
            action = request.form.get("action", "add")
            if action == "add":
                workpiece_id = request.form.get("workpiece_id", "")
                price = request.form.get("price_" + workpiece_id, "")
                quantity = request.form.get("quantity_" + workpiece_id, "")
                if not price or not quantity:
                    raise ValueError("Введите цену и количество.")
                line = invoice_line({
                    "workpiece_id": workpiece_id,
                    "price": price,
                    "quantity": quantity,
                })
                draft["lines"].append(line)
            elif action.startswith("remove:"):
                index = int(action.split(":", 1)[1])
                draft["lines"].pop(index)
            elif action == "clear":
                draft["lines"] = []
            elif action == "accept":
                invoice_id = save_invoice(provider, draft)
                session.pop("invoice_draft", None)
                return render_template("invoice_success.html", invoice_id=invoice_id)
            session["invoice_draft"] = draft
            return redirect(url_for("invoice_bp.invoice_index"))
    except ValueError as exc:
        error = str(exc)
        status_code = 400
    except Error:
        current_app.logger.exception("Ошибка приёмки поставки")
        error = "База данных недоступна или поставку не удалось сохранить. Черновик сохранён. Попробуйте ещё раз."
        status_code = 503

    names = {item["id"]: item["name"] for item in workpieces}
    total = sum((line_total(line) for line in draft["lines"]), Decimal("0.00"))
    return render_template(
        "invoice_form.html", draft=draft, suppliers=suppliers, workpieces=workpieces,
        names=names, total=total, line_total=line_total, error=error,
        values=request.form if request.method == "POST" else {},
    ), status_code

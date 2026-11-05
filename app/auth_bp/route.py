from pathlib import Path

from flask import Blueprint, redirect, render_template, request, url_for

from app.auth_bp.model_route import model_route
from app.db.sql_provider import SQLProvider


blueprint_auth = Blueprint("auth_bp", __name__, template_folder="templates")
provider = SQLProvider(Path(__file__).parent / "sql")


@blueprint_auth.route("/", methods=["GET", "POST"])
def auth_index():
    if request.method == "POST":
        response = model_route(provider, request.form)
        if response.status:
            return redirect(url_for("main_menu"))
        return render_template(
            "login.html", login=request.form.get("login", ""),
            error=response.err_message,
        ), response.status_code
    return render_template("login.html", login="")

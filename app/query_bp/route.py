from pathlib import Path

from flask import Blueprint, abort, render_template, request

from app.db.sql_provider import SQLProvider
from app.query_bp.model_route import QUERIES, model_route


blueprint_query = Blueprint("query_bp", __name__, template_folder="templates")
provider = SQLProvider(Path(__file__).parent / "sql")


@blueprint_query.route("/")
def query_menu_handler():
    return render_template("query_menu.html", queries=QUERIES)


@blueprint_query.route("/<query_name>", methods=["GET", "POST"])
def query_handler(query_name):
    if query_name not in QUERIES:
        abort(404)
    query = QUERIES[query_name]
    values = request.form.to_dict() if request.method == "POST" else {}
    if request.method == "POST":
        response = model_route(provider, query_name, values)
        if response.status:
            return render_template(
                "query_result.html", query=query, query_name=query_name,
                rows=response.result,
            )
        return render_template(
            query["template"], query=query, query_name=query_name,
            values=values, error=response.err_message,
        ), response.status_code
    return render_template(
        query["template"], query=query, query_name=query_name, values=values,
    )

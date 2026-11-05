import json
import os
from pathlib import Path
from secrets import token_hex

from flask import Flask, render_template, session

from app.access import login_required
from app.auth_bp.route import blueprint_auth
from app.query_bp.route import blueprint_query


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or token_hex(32)
app.register_blueprint(blueprint_query, url_prefix="/query")
app.register_blueprint(blueprint_auth, url_prefix="/auth")

with (Path(__file__).parent / "data" / "access.json").open(encoding="utf-8") as access_file:
    app.config["db_access"] = json.load(access_file)

config_path = Path(__file__).parent / "data" / "db_config.json"
if config_path.is_file():
    with config_path.open(encoding="utf-8") as config_file:
        app.config["db_config"] = json.load(config_file)


@app.route("/")
@login_required
def main_menu():
    return render_template("main_menu.html")


@app.route("/exit")
def exit_func():
    session.clear()
    return render_template("exit.html")


@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html"), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run()

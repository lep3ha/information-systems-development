import json
from pathlib import Path

from flask import Flask, render_template

from app.query_bp.route import blueprint_query


app = Flask(__name__)
app.register_blueprint(blueprint_query, url_prefix="/query")

config_path = Path(__file__).parent / "data" / "db_config.json"
if config_path.is_file():
    with config_path.open(encoding="utf-8") as config_file:
        app.config["db_config"] = json.load(config_file)


@app.route("/")
def main_menu():
    return render_template("main_menu.html")


@app.route("/exit")
def exit_func():
    return render_template("exit.html")


if __name__ == "__main__":
    app.run()

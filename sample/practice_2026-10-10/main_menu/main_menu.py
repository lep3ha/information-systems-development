import json
from flask import Flask, render_template
from query_bp.route import blueprint_query

app = Flask(__name__)
app.register_blueprint(blueprint_query, url_prefix='/query')


with open('../data/db_config.json', 'r') as f:
    app.config["db_config"] = json.load(f)


@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/exit')
def exit_func():
    return 'До свидания'

if __name__ == '__main__':
    app.run(debug=True)
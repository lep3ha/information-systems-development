import json
from flask import Flask, render_template, session
from query_blueprint.route import blueprint_query
from auth_blueprint.route import blueprint_auth
from access import login_required


app = Flask(__name__)
app.secret_key = 'You will never guess'

app.register_blueprint(blueprint_query, url_prefix='/query')
app.register_blueprint(blueprint_auth, url_prefix='/auth')

with open('../data/db_config.json', 'r', encoding='utf-8') as f:
    db_config = json.load(f)
    app.config['db_config'] = db_config

with open('../data/access.json', 'r', encoding='utf-8') as f:
    access = json.load(f)
    app.config['db_access'] = access


@app.route('/')
@login_required
def main_menu():
    return render_template('main_menu.html')

@app.route('/exit')
def exit_func():
    session.clear()
    return 'До свидания'


if __name__ == '__main__':
    app.run(debug=True)
import os, json, sys
from flask import Flask, render_template, g, session

# Принудительно устанавливаем UTF-8
if sys.platform.startswith('win'):
    os.system('chcp 65001 > nul')

BASE_DIR = os.path.dirname(__file__)

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = 'dev'

# Настройки кодировки
app.config['JSON_AS_ASCII'] = False
app.config['ENCODING'] = 'utf-8'

# Загрузка конфигураций
with open(os.path.join(BASE_DIR, 'config', 'db_config.json'), 'r', encoding='utf-8') as f:
    app.config['db_config'] = json.load(f)

with open(os.path.join(BASE_DIR, 'config', 'access.json'), 'r', encoding='utf-8') as f:
    app.config['access_config'] = json.load(f)

# Регистрируем blueprint'ы
from auth.routes import auth_bp
from queries.routes import queries_bp
from reports.routes import reports_bp
from basket.routes import basket_bp

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(queries_bp, url_prefix='/queries')
app.register_blueprint(reports_bp, url_prefix='/reports')
app.register_blueprint(basket_bp, url_prefix='/basket')

from auth.access import login_required

@app.before_request
def before_request():
    g.encoding = 'utf-8'

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

@app.route('/', methods=['GET'])
@login_required
def main_menu():
    return render_template('main_menu.html')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True)
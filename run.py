from flask import Flask, render_template, session

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.secret_key = 'your-secret-key-here'

# Регистрация блюпринтов
from app.data.routes import data
app.register_blueprint(data, url_prefix='/monitoring')

from app.auth.routes import auth
app.register_blueprint(auth, url_prefix='/auth')
 
from app.cart.routes import cart
app.register_blueprint(cart, url_prefix='/cart')
 
from app.analytics.routes import analytics
app.register_blueprint(analytics, url_prefix='/analytics')

@app.route('/')
def main():
    if session.get('user_id'):
        return render_template("main_authenticated.html")
    return render_template("main_guest.html")

@app.route('/away')
def away():
    return render_template("away.html")

from app.auth.access import permission_required
@app.route('/panel')
@permission_required('monitoring_viewer')
def panel():
    return render_template("admin_panel.html")

@app.errorhandler(403)
def forbidden(error = None):
    return render_template("base/http_forbidden.html"), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5005)
from flask import Flask, render_template, current_app, Blueprint, request, redirect, url_for
from database_clone.sql_provider import SQLProvider
from os import path
from auth_blueprint.model_route import model_route


blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth_index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        params = dict(request.form)
        response = model_route(provider, params)
        if response.status:
            return redirect(url_for('main_menu'))
        else:
            return 'Something happened'

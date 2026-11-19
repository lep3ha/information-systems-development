import os
from flask import render_template, request, Blueprint, session, redirect, url_for, current_app
from database_clone.sql_provider import SQLProvider
from auth_blueprint.model_route import model_route

blueprint_auth = Blueprint('auth_bp', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth_index():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user_input = dict(request.form)
        response = model_route(provider, user_input)
        if response.status:
            return redirect(url_for('main_menu'))
        else:
            return response.err_message





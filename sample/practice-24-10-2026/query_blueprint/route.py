from flask import Flask, render_template, current_app, Blueprint, request
from database_clone.sql_provider import SQLProvider
from os import path
from query_blueprint.model_route import model_route
from access import login_required, group_required


blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


@blueprint_query.route('/')
@login_required
@group_required
def query_menu():
    return render_template('query_menu.html')


@blueprint_query.route('/query1', methods=['GET'])
@login_required
@group_required
def product_handler_form():
    return render_template('input_form.html')


@blueprint_query.route('/query1', methods=['POST'])
@login_required
@group_required
def product_handler_result():
    params = dict(request.form)
    response = model_route(provider, params)
    if response.status:
        return render_template('result.html', prod_title='Результат', products=response.result)
    else:
        return f'Что-то пошло не так, {response.err_mesage}'


if __name__ == '__main__':
    app.run(debug=True)
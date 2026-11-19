from flask import Flask, render_template, Blueprint, request
from database.select import select_dict
from database.sql_provider import SQLProvider
from os import path
from query_bp.model_route import model_route

blueprint_query = Blueprint('query_bp', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


@blueprint_query.route('/')
def query_menu_handler():
    return render_template('query_menu.html')

@blueprint_query.route('/execute', methods=['GET'])
def query_handler():
    return render_template('query1.html')

@blueprint_query.route('/execute', methods=['POST'])
def query_executor():
    params = dict(request.form)
    response = model_route(provider, params)

    if response.status:
        return render_template('query_result.html', prod_title='Продукты' , product=response.result)
    else:
        return f'Что-то пошло не так, {response.err_message}'

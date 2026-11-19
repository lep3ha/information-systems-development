import os
from datetime import datetime
from flask import render_template, Blueprint, request, current_app, session, url_for, redirect
from database_clone.sql_provider import SQLProvider
from database_clone.select import select_dict, select_list, execute_insert
from cache.wrapper import fetch_from_cache


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', methods=['GET', 'POST'])
def order_index():
    cache_config = current_app.config['cache_config']
    cache_select = fetch_from_cache('some_items_cashed', cache_config)(select_dict)
    if request.method == 'GET':
        sql = provider.get('all_items.sql')
        # items = select_dict(sql, {})
        items = cache_select(sql, {})
        basket_items = session.get('basket', {})
        return render_template('basket_order_list.html', items=items, basket=basket_items)
    else:
        prod_id = request.form.get('prod_id')
        user_dict = dict(request.form)
        user_dict1 = user_dict.pop('send')
        print('user_dict=', user_dict)
        sql = provider.get('added_item.sql')
        item = select_dict(sql, user_dict)[0]
        print('item in route=', item)
        add_to_basket(item, prod_id)

    return redirect(url_for('bp_order.order_index'))


def add_to_basket(item: dict, prod_id):
    current_basket = session.get('basket', {})
    print('current_basket=', current_basket)
    if prod_id in current_basket:
        current_basket[prod_id]['amount'] += 1
    else:
        current_basket[prod_id] = {
            'prod_name': item['prod_name'],
            'prod_price': item['prod_price'],
            'amount': 1}
        session['basket'] = current_basket
        print('current_basket_new=', current_basket)
        session.permanent = True
    return True


@blueprint_order.route('/clear_basket')
def clear_basket():
    session.pop('basket')
    return redirect(url_for('bp_order.order_index'))

@blueprint_order.route('/create_order')
def create_order():
    current_basket = session.get('basket', {})
    now_dt = datetime.now().strftime('%Y-%m-%d')
    user_id = session['user_id']
    insert_order = '''
    insert into user_orders(user_id, order_date) values (%s, %s) returning order_id
    '''
    last_order_id = execute_insert(insert_order, {'user_id': user_id, 'now_dt': now_dt})
    print('last_order_id = ', last_order_id)

    insert_rows = '''
    insert into order_lines(order_id, prod_id, prod_amt) values (%s, %s, %s) returning line_id
    '''
    for item, item_characteristics in current_basket.items():
        insert_params = {
            'order_id': int(last_order_id),
            'prod_id': int(item),
            'prod_amt': item_characteristics['amount']
        }
        execute_insert(insert_rows, insert_params)

    clear_basket()
    return redirect(url_for('bp_order.order_index'))



from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.cart.model import CartModel
from app.cart.forms import UpdateCartItemForm
from app.auth.access import login_required

cart = Blueprint('cart', __name__, template_folder='templates')
model = CartModel()


@cart.route('/', methods=['GET'])
@login_required
def index():
    return redirect(url_for('cart.catalog'))


@cart.route('/catalog', methods=['GET'])
@login_required
def catalog():
    result = model.get_catalog()
    items = result['data'] if result['status'] else []
    return render_template('cart/catalog.html', items=items, title='Каталог')


@cart.route('/add', methods=['POST'])
@login_required
def add_to_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity', '1')
        price_at_add = request.form.get('price_at_add')

        if not product_id or not price_at_add:
            flash('Некорректные данные формы', 'warning')
            return redirect(url_for('cart.catalog'))

        user_id = session.get('user_id')
        res = model.add_to_cart(user_id, int(product_id), int(quantity), float(price_at_add))
        if res.get('status'):
            flash('Товар добавлен в корзину', 'success')
        else:
            flash(res.get('msg', 'Ошибка добавления в корзину'), 'danger')
    except Exception as e:
        flash('Ошибка при добавлении в корзину: ' + str(e), 'danger')

    return redirect(url_for('cart.catalog'))


@cart.route('/view', methods=['GET', 'POST'])
@login_required
def view_cart():
    user_id = session.get('user_id')
    form = UpdateCartItemForm()
    cart_res = model.get_cart(user_id)
    items = cart_res['data'] if cart_res['status'] else []
    total = sum([it['price'] * it['quantity'] for it in items]) if items else 0
    return render_template('cart/cart.html', items=items, total=total, form=form, title='Корзина')


@cart.route('/update', methods=['POST'])
@login_required
def update_item():
    form = UpdateCartItemForm()
    if form.validate_on_submit():
        res = model.update_item(int(form.item_id.data), int(form.quantity.data))
        if res['status']:
            flash('Количество обновлено', 'success')
        else:
            flash(res.get('msg', 'Ошибка обновления'), 'danger')
    else:
        flash('Некорректные данные формы', 'warning')
    return redirect(url_for('cart.view_cart'))


@cart.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_item(item_id):
    res = model.remove_item(item_id)
    if res['status']:
        flash('Позиция удалена', 'info')
    else:
        flash(res.get('msg', 'Ошибка удаления'), 'danger')
    return redirect(url_for('cart.view_cart'))


@cart.route('/checkout', methods=['POST'])
@login_required
def checkout():
    user_id = session.get('user_id')
    res = model.checkout(user_id)
    if res['status']:
        flash('Заказ оформлен', 'success')
        return render_template('cart/checkout_confirmation.html', order_id=res['data']['order_id'])
    else:
        flash(res.get('msg', 'Ошибка оформления заказа'), 'danger')
        return redirect(url_for('cart.view_cart'))

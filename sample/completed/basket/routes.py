from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from auth.access import login_required
from .models import basket_model

basket_bp = Blueprint('basket', __name__, template_folder='templates')

@basket_bp.route('/', methods=['GET'])
def basket():
    """Отображение корзины и списка товаров"""
    try:
        products = basket_model.get_all_products()
        basket_session = session.get('basket', {})
        total_price = calculate_total_price(basket_session)

        return render_template('basket.html',
                             products=products,
                             basket=basket_session,
                             total_price=total_price)
    except Exception as e:
        flash(f'Ошибка при загрузке товаров: {str(e)}', 'error')
        return render_template('basket.html', products=[], basket={}, total_price=0)

@basket_bp.route('/add/<int:product_id>', methods=['POST'])
def add_to_basket(product_id):
    """Добавление товара в корзину"""
    try:
        # Получаем информацию
        product = basket_model.get_product_by_id(product_id)

        if not product:
            flash('Товар не найден', 'error')
            return redirect(url_for('basket.basket'))

        if 'basket' not in session:
            session['basket'] = {}

        basket_session = session['basket']
        product_id_str = str(product_id)

        if product_id_str in basket_session:
            # Увеличиваем количество, если товар уже в корзине
            basket_session[product_id_str]['amount'] += 1
        else:
            # Добавляем новый товар
            basket_session[product_id_str] = {
                'product_name': product['product_name'],
                'price': float(product['price']),
                'category_name': product['category_name'],
                'amount': 1
            }

        session['basket'] = basket_session
        session.modified = True

        flash(f'Товар "{product["product_name"]}" добавлен в корзину', 'success')
        return redirect(url_for('basket.basket'))

    except Exception as e:
        flash(f'Ошибка при добавлении товара: {str(e)}', 'error')
        return redirect(url_for('basket.basket'))

@basket_bp.route('/update/<int:product_id>', methods=['POST'])
def update_basket_item(product_id):
    """Обновление количества товара в корзине"""
    try:
        new_amount = int(request.form.get('amount', 1))

        if new_amount <= 0:
            return remove_from_basket(product_id)

        basket_session = session.get('basket', {})
        product_id_str = str(product_id)

        if product_id_str in basket_session:
            basket_session[product_id_str]['amount'] = new_amount
            session['basket'] = basket_session
            session.modified = True
            flash('Количество товара обновлено', 'success')

        return redirect(url_for('basket.basket'))

    except Exception as e:
        flash(f'Ошибка при обновлении товара: {str(e)}', 'error')
        return redirect(url_for('basket.basket'))

@basket_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_basket(product_id):
    """Удаление товара из корзины"""
    basket_session = session.get('basket', {})
    product_id_str = str(product_id)

    if product_id_str in basket_session:
        product_name = basket_session[product_id_str]['product_name']
        del basket_session[product_id_str]
        session['basket'] = basket_session
        session.modified = True
        flash(f'Товар "{product_name}" удален из корзины', 'success')

    return redirect(url_for('basket.basket'))

@basket_bp.route('/clear', methods=['POST'])
def clear_basket():
    """Очистка корзины"""
    session['basket'] = {}
    session.modified = True
    flash('Корзина очищена', 'success')
    return redirect(url_for('basket.basket'))

@basket_bp.route('/checkout', methods=['POST'])
@login_required
def checkout():
    """Оформление заказа"""
    basket_session = session.get('basket', {})

    if not basket_session:
        flash('Корзина пуста', 'error')
        return redirect(url_for('basket.basket'))

    try:
        # Сохраняем заказ в БД
        order_id = basket_model.save_order(basket_session, session.get('user_id'))

        session['basket'] = {}
        session.modified = True

        flash(f'Заказ успешно оформлен! Номер заказа: {order_id}', 'success')
        return render_template('order_success.html', order_id=order_id)

    except Exception as e:
        flash(f'Ошибка при оформлении заказа: {str(e)}', 'error')
        return redirect(url_for('basket.basket'))

def calculate_total_price(basket):
    """Расчет общей стоимости корзины"""
    total = 0
    for item in basket.values():
        total += item['price'] * item['amount']
    return total
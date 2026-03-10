from app.db.context_manager import DBContextManager
from app.db.sql_provider import SQLProvider


class CartModel:
    def __init__(self):
        self.sql_provider = SQLProvider('app/cart/sql')

    def get_catalog(self):
        try:
            sql = self.sql_provider.get('catalog.sql')
            with DBContextManager() as db:
                db.execute(sql)
                rows = db.fetchall()
                columns = [desc[0] for desc in db.description]
                items = []
                for r in rows:
                    items.append(dict(zip(columns, r)))
                return {'status': True, 'data': items}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': []}

    def _ensure_cart(self, user_id):
        try:
            with DBContextManager() as db:
                db.execute('SELECT id FROM carts WHERE user_id = %s', (user_id,))
                row = db.fetchone()
                if row:
                    return row[0]
                db.execute('INSERT INTO carts (user_id) VALUES (%s) RETURNING id', (user_id,))
                return db.fetchone()[0]
        except Exception:
            raise

    def add_to_cart(self, user_id, product_id, quantity, price_at_add):
        try:
            cart_id = self._ensure_cart(user_id)
            sql = self.sql_provider.get('add_to_cart.sql')
            with DBContextManager() as db:
                db.execute(sql, (cart_id, product_id, quantity, price_at_add))
                row = db.fetchone()
                return {'status': True, 'data': {'item_id': row[0] if row else None}}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

    def get_cart(self, user_id):
        try:
            cart_id = self._ensure_cart(user_id)
            sql = self.sql_provider.get('get_cart.sql')
            with DBContextManager() as db:
                db.execute(sql, (cart_id,))
                rows = db.fetchall()
                columns = [desc[0] for desc in db.description]
                items = [dict(zip(columns, r)) for r in rows]
                return {'status': True, 'data': items, 'cart_id': cart_id}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': []}

    def update_item(self, item_id, quantity):
        try:
            sql = self.sql_provider.get('update_cart_item.sql')
            with DBContextManager() as db:
                db.execute(sql, (quantity, item_id))
                row = db.fetchone()
                return {'status': True, 'data': {'item_id': row[0] if row else None}}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

    def remove_item(self, item_id):
        try:
            sql = self.sql_provider.get('remove_cart_item.sql')
            with DBContextManager() as db:
                db.execute(sql, (item_id,))
                return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

    def checkout(self, user_id):
        try:
            cart_res = self.get_cart(user_id)
            if not cart_res['status']:
                return {'status': False, 'msg': cart_res.get('msg', 'Ошибка получения корзины')}

            items = cart_res['data']
            if not items:
                return {'status': False, 'msg': 'Корзина пуста'}

            create_order_sql = self.sql_provider.get('create_order.sql')
            add_order_item_sql = self.sql_provider.get('add_order_item.sql')
            clear_cart_sql = self.sql_provider.get('clear_cart_items.sql')

            with DBContextManager() as db:
                # Создать заказ
                db.execute(create_order_sql, (user_id,))
                order_id = db.fetchone()[0]

                # Добавить элементы заказа (триггер уменьшит склад)
                for it in items:
                    db.execute(add_order_item_sql, (order_id, it['product_id'], it['quantity'], it['price_at_add']))

                # Очистить корзину
                db.execute(clear_cart_sql, (cart_res['cart_id'],))

                return {'status': True, 'data': {'order_id': order_id}}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

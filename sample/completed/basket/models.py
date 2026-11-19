from database.select import select_list
from database.DBcm import DBContextManager
from database.sql_provider import SQLProvider
from flask import current_app


class BasketModel:
    def __init__(self):
        self.sql_provider = SQLProvider('SQL/basket')

    def get_all_products(self):
        """Получает все доступные товары"""
        try:
            sql = self.sql_provider.get('get_products.sql')
            return select_list(sql)
        except Exception as e:
            print(f"Ошибка при получении товаров: {e}")
            return []

    def get_product_by_id(self, product_id):
        """Получает товар по ID"""
        try:
            sql = self.sql_provider.get('get_product_by_id.sql')
            result = select_list(sql, [product_id])
            return result[0] if result else None
        except Exception as e:
            print(f"Ошибка при получении товара: {e}")
            return None

    def save_order(self, basket, user_id):
        """Сохраняет заказ в базу данных"""
        try:
            cfg = current_app.config['db_config']

            with DBContextManager(cfg) as cursor:
                # Создаем основной заказ
                sql_order = self.sql_provider.get('create_order.sql')
                cursor.execute(sql_order, (user_id,))
                order_id = cursor.lastrowid

                # Добавляем товары заказа
                sql_items = self.sql_provider.get('create_order_items.sql')
                for product_id_str, item in basket.items():
                    product_id = int(product_id_str)
                    cursor.execute(sql_items, (order_id, product_id, item['amount'], item['price']))

                return order_id

        except Exception as e:
            print(f"Ошибка при сохранении заказа: {e}")
            raise e


# Создаем экземпляр модели
basket_model = BasketModel()
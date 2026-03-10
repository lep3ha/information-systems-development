from app.db.context_manager import DBContextManager
from app.db.sql_provider import SQLProvider
import datetime

class FetchModel:
    def __init__(self):
        self.sql_provider = SQLProvider('app/data/sql')
    
    def get_categories(self):
        """Получение списка категорий продуктов"""
        try:
            with DBContextManager() as db:
                db.execute(self.sql_provider.get("select_material.sql"))
                result = db.fetchall()
                
                categories = []
                for row in result:
                    categories.append({
                        'category': row[0]
                    })
                
                return {'status': True, 'data': categories}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения категорий: {str(e)}', 'data': []}
    
    def get_products(self, params):
        """Получение товаров с фильтрацией"""
        translated = {
            "id": "ID",
            "product_code": "Артикул",
            "name": "Название",
            "category": "Категория",
            "weight": "Вес, кг.",
            "price": "Себестоимость, руб.",
            "quantity": "В наличии, шт.",
        }
        try:
            # Валидация параметров
            validated_params = self._validate_product_params(params)
            
            # Получаем SQL с параметрами
            sql = self.sql_provider.get("filter_items.sql", **validated_params)
            with DBContextManager() as db:
                db.execute(sql)
                result = db.fetchall()
                
                # Получаем названия колонок
                columns = [translated[desc[0]] for desc in db.description]

                
                # Преобразуем в список словарей
                items = []
                for row in result:
                    item = {}
                    for i, col in enumerate(columns):
                        item[col] = row[i]
                    items.append(item)
                
                return {'status': True, 'data': items}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения товаров: {str(e)}', 'data': []}
    
    def _validate_product_params(self, params):
        """Валидация и нормализация параметров"""
        validated = {
            "category": params.get("category", "") or "",
            "min_price": float(params.get("min_price", 0)) or 0,
            "max_price": float(params.get("max_price", 0)) or 0,
            "sort_by": params.get("sort_by", "name_asc") or "name_asc"
        }
        
        # Проверяем, что max_price >= min_price
        if validated["max_price"] > 0 and validated["max_price"] < validated["min_price"]:
            validated["max_price"] = 0 
        
        return validated
    

    def get_cities(self):
        """Получение списка уникальных городов поставщиков"""
        try:
            with DBContextManager() as db:
                db.execute(self.sql_provider.get("select_city.sql"))
                result = db.fetchall()
                
                cities = []
                for row in result:
                    cities.append({
                        'city': row[0]
                    })
                
                return {'status': True, 'data': cities}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения городов: {str(e)}', 'data': []}
    
    def get_suppliers_list(self):
        """Получение списка всех поставщиков для фильтра"""
        try:
            with DBContextManager() as db:
                db.execute(self.sql_provider.get("select_suppliers_list.sql"))
                result = db.fetchall()
                
                suppliers = [("0", "Все")]
                for row in result:
                    suppliers.append((str(row[0]), row[1]))
                
                return {'status': True, 'data': suppliers}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения поставщиков: {str(e)}', 'data': []}
    
    def get_suppliers(self, params):
        """Получение поставщиков с фильтрацией"""
        translated = {
            "id": "ID",
            "name": "Название",
            "city": "Город",
            "contract_date": "Дата контракта",
            "invoice_count": "Кол-во поставок",
            "total_invoices": "Общая сумма поставок"
        }
        try:
            validated_params = self._validate_supplier_params(params)
        
            sql = self.sql_provider.get("filter_suppliers.sql", **validated_params)
            
            with DBContextManager() as db:
                db.execute(sql)
                result = db.fetchall()
                
                columns = [translated[desc[0]] for desc in db.description]
                
                items = []
                for row in result:
                    item = {}
                    for i, col in enumerate(columns):
                        item[col] = row[i]
                    items.append(item)
                
                return {'status': True, 'data': items}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения поставщиков: {str(e)}', 'data': []}
    
    def get_invoices(self, params):
        """Получение накладных с фильтрацией"""
        translated = {
            "id": "ID",
            "supplier_name": "Поставщик",
            "delivery_date": "Дата поставки",
            "total_cost": "Сумма, руб.",
            "item_count": "Кол-во позиций",
            "total_quantity": "Общее кол-во"
        }
        try:
            validated_params = self._validate_invoice_params(params)
            
            sql = self.sql_provider.get("filter_invoices.sql", **validated_params)
            with DBContextManager() as db:
                db.execute(sql)
                result = db.fetchall()
                
                columns = [translated[desc[0]] for desc in db.description]
                
                items = []
                for row in result:
                    item = {}
                    for i, col in enumerate(columns):
                        item[col] = row[i]
                    items.append(item)
                
                return {'status': True, 'data': items}
        except Exception as e:
            return {'status': False, 'msg': f'Ошибка получения накладных: {str(e)}', 'data': []}
    
    def _validate_supplier_params(self, params):
        """Валидация параметров для поставщиков"""
        validated = {
            "city": params.get("city", "") or "",
            "min_date": params.get("min_contract_date", "01.01.1970"),
            "max_date": params.get("max_contract_date", datetime.datetime.now().strftime('%Y-%m-%d')),
            "sort_by": params.get("sort_by", "name_asc") or "name_asc"
        }

        # Нормализация дат
        if validated["min_date"] and hasattr(validated["min_date"], 'strftime'):
            validated["min_date"] = validated["min_date"].strftime('%Y-%m-%d')
        elif not validated["min_date"]:
            validated["min_date"] = "01.01.1970"
        
        if validated["max_date"] and hasattr(validated["max_date"], 'strftime'):
            validated["max_date"] = validated["max_date"].strftime('%Y-%m-%d')
        elif not validated["max_date"]:
            validated["max_date"] = datetime.datetime.now().strftime('%Y-%m-%d')
        
        return validated
    
    def _validate_invoice_params(self, params):
        """Валидация параметров для накладных"""
        validated = {
            "supplier_id": int(params.get("supplier_id", 0)) or 0,
            "min_date": params.get("min_delivery_date", "01.01.1970"),
            "max_date": params.get("max_delivery_date", datetime.datetime.now().strftime('%Y-%m-%d')),
            "min_total": float(params.get("min_total_cost", 0)) or 0,
            "max_total": float(params.get("max_total_cost", 100000)) or 100000,
            "sort_by": params.get("sort_by", "date_desc") or "date_desc"
        }
        # Нормализация дат
        if validated["min_date"] and hasattr(validated["min_date"], 'strftime'):
            validated["min_date"] = validated["min_date"].strftime('%Y-%m-%d')
        elif not validated["min_date"]:
            validated["min_date"] = "01.01.1970"
        
        if validated["max_date"] and hasattr(validated["max_date"], 'strftime'):
            validated["max_date"] = validated["max_date"].strftime('%Y-%m-%d')
        elif not validated["max_date"]:
            validated["max_date"] = datetime.datetime.now().strftime('%Y-%m-%d')
    
        # Проверка суммы
        if validated["max_total"] > 0 and validated["max_total"] < validated["min_total"]:
            validated["max_total"] = 100000
        
        return validated
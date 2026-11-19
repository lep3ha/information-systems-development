from database.select import select_list
from database.sql_provider import SQLProvider

class QueriesModel:
    def __init__(self):
        self.sql_provider = SQLProvider('SQL/queries')

    def get_products_by_category(self, category_id):
        try:
            sql = self.sql_provider.get('products_by_category.sql')
            return select_list(sql, [category_id])
        except Exception as e:
            print(f"Error in get_products_by_category: {e}")
            return []

queries_model = QueriesModel()
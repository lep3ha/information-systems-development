from database.select import select_one
from database.sql_provider import SQLProvider

class AuthModel:
    def __init__(self):
        self.sql_provider = SQLProvider('SQL/auth')

    def authenticate_user(self, username, password):
        sql = self.sql_provider.get('auth.sql')
        return select_one(sql, {'login': username, 'pass': password})

auth_model = AuthModel()
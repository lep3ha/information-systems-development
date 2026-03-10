from app.db.context_manager import DBContextManager
from app.db.sql_provider import SQLProvider
import hashlib

class AuthModel:
    def __init__(self):
        self.sql_provider = SQLProvider('app/auth/sql')
    
    def authenticate(self, username, password):
        try:
            sql = self.sql_provider.get('authenticate.sql')
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            
            with DBContextManager() as db:
                db.execute(sql, (username, hashed_pw))
                user = db.fetchone()
                
                if user:
                    columns = [desc[0] for desc in db.description]
                    return {'status': True,'msg': f'Добро пожаловать, {username if user[2] is None else user[2]}', 'data': dict(zip(columns, user))}
                return {'status': False, 'msg': 'Неверный логин или пароль', 'data': {}}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': {}}
    
    def register_user(self, username, first_name, second_name, password):
        try:
            sql_reg = self.sql_provider.get('register.sql')
            sql_check = self.sql_provider.get('authenticate.sql')

            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            
            with DBContextManager() as db:
                db.execute(sql_check, (username, hashed_pw))
                existing = db.fetchone()
                if existing:
                    return {'status': False, 'msg': 'Пользователь с таким именем уже существует', 'data': {}}

                db.execute(sql_reg, (username, first_name, second_name, hashed_pw))
                user_id = db.fetchone()[0]
                return {'status': True, 'msg': f'Регистрация прошла успешно', 'data': {'id': user_id}}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': {}}
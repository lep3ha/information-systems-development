from functools import wraps
from flask import session, redirect, url_for, current_app, request, flash

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))  # Исправлено с 'auth_bp.login'

    return wrapper

def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            access = current_app.config.get('access_config', {})
            user_request = request.endpoint
            user_role = session.get('user_group', 'user')

            if user_role in access and user_request in access[user_role]:
                return func(*args, **kwargs)
            else:
                flash('Доступ запрещен', 'error')
                return redirect(url_for('main_menu'))
        return redirect(url_for('auth.login'))  # Исправлено с 'auth_bp.login'

    return wrapper
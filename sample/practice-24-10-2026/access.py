from functools import wraps
from flask import session, redirect, url_for, current_app, request


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth_bp.auth_index'))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_group' in session:
            access = current_app.config['db_access']
            user_request = request.endpoint.split('.')[0]
            # query_bp.query_menu -> ['query_bp', 'query_menu'] -> query_bp
            user_role = session['user_group']
            if user_role in access and user_request in access[user_role]:
                return func(*args, **kwargs)
            else:
                return 'You have no access'
        return redirect(url_for('auth_bp.auth_index'))
    return wrapper
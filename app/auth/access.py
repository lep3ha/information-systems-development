from functools import wraps
from flask import session, redirect, url_for, flash, render_template, abort
from app.db.context_manager import DBContextManager

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Требуется авторизация', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def permission_required(*perms):
    """
    Декоратор для проверки разрешений пользователя.

    Принимает одну либо несколько строк вида "permission_role" либо список/кортеж таких строк.
    Разрешение даётся, если у пользователя есть хотя бы одно указанное сочетание.

    Примеры использования:
      @permission_required('reports_viewer')
      @permission_required('reports_creator', 'reports_editor')
      @permission_required(*['reports_creator','reports_editor'])
    """

    # Если декоратор применён без скобок (как @permission_required),
    # то первый элемент будет callable (функция) — это неверное использование.
    if len(perms) == 1 and callable(perms[0]):
        raise TypeError("permission_required must be called with permission strings, e.g. @permission_required('perm_role')")

    # Поддерживаем вызов с одним аргументом-списком/кортежем
    if len(perms) == 1 and isinstance(perms[0], (list, tuple, set)):
        perms_list = list(perms[0])
    else:
        perms_list = list(perms)

    # Убедимся, что каждый элемент — строка
    perms_list = [str(p) for p in perms_list]

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Требуется авторизация', 'warning')
                return redirect(url_for('auth.login'))

            user_id = session.get('user_id')

            try:
                with DBContextManager() as db:
                    for perm in perms_list:
                        parts = perm.rsplit('_', 1)
                        if len(parts) != 2:
                            flash('Ошибка конфигурации разрешения', 'danger')
                            return render_template('base/http_forbidden.html'), 403

                        permission_name, role_name = parts
                        query = """
                            SELECT EXISTS(
                                SELECT 1 FROM user_permission up
                                WHERE up.user_id = %s
                                  AND up.permission = %s
                                  AND up.role = %s
                            )
                        """
                        db.execute(query, (user_id, permission_name, role_name))
                        exists_row = db.fetchone()
                        exists = exists_row[0] if exists_row else False
                        if exists:
                            return f(*args, **kwargs)

                    # Ни одного совпадения не найдено
                    abort(403)
            except TypeError as e:
                # Частая причина — неверный тип perm (например, передали функцию)
                print(f"[PERMISSION ERROR] TypeError при проверке разрешения: {e}")
                abort(403)
            except Exception as e:
                print(f"[PERMISSION ERROR] Ошибка проверки разрешения: {e}")
                abort(403)

        return decorated_function

    return decorator
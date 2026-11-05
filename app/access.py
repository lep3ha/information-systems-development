from functools import wraps

from flask import abort, current_app, redirect, request, session, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_group" in session:
            return func(*args, **kwargs)
        return redirect(url_for("auth_bp.auth_index"))
    return wrapper


def group_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_group" not in session:
            return redirect(url_for("auth_bp.auth_index"))
        blueprint = request.blueprint
        access = current_app.config["db_access"]
        if blueprint not in access.get(session["user_group"], []):
            abort(403)
        return func(*args, **kwargs)
    return wrapper

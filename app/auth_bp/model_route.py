from dataclasses import dataclass

from flask import current_app, session
from psycopg2 import Error
from werkzeug.security import check_password_hash

from app.db.select import select_list


@dataclass
class ResultInfo:
    status: bool
    err_message: str = ""
    status_code: int = 200


def model_route(provider, values):
    login = values.get("login", "")
    password = values.get("password", "")
    if not login or not password or "\x00" in login:
        return ResultInfo(False, "Введите логин и пароль.", 400)
    if "db_config" not in current_app.config:
        current_app.logger.error("Не загружен файл app/data/db_config.json")
        return ResultInfo(False, "База данных недоступна. Попробуйте позже.", 503)
    try:
        rows = select_list(provider.get("internal_user.sql"), {"login": login})
    except Error:
        current_app.logger.exception("Ошибка авторизации: база данных недоступна")
        return ResultInfo(False, "База данных недоступна. Попробуйте позже.", 503)
    if not rows or not check_password_hash(rows[0]["password_hash"], password):
        return ResultInfo(False, "Неверный логин или пароль.", 401)
    user = rows[0]
    session.clear()
    session["user_id"] = user["user_id"]
    session["user_group"] = user["user_group"]
    session.permanent = True
    return ResultInfo(True)

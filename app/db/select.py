from flask import current_app

from app.db.context_manager import DBContextManager


def select_list(sql, params):
    with DBContextManager(current_app.config["db_config"]) as cursor:
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
    return rows, columns


def select_dict(sql, params):
    rows, columns = select_list(sql, list(params.values()))
    return [dict(zip(columns, row)) for row in rows]

from flask import current_app

from app.db.context_manager import DBContextManager


def select_list(sql, params):
    with DBContextManager(current_app.config["db_config"]) as cursor:
        cursor.execute(sql, list(params.values()))
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

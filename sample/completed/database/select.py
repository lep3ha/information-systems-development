from flask import current_app
from .DBcm import DBContextManager

def select_list(sql: str, params=None):
    params = params or []
    cfg = current_app.config['db_config']

    try:
        with DBContextManager(cfg) as cur:
            cur.execute(sql, params)
            columns = [desc[0] for desc in cur.description]

            results = []
            for row in cur.fetchall():
                row_dict = {}
                for i, col in enumerate(columns):
                    value = row[i]
                    row_dict[col] = value
                results.append(row_dict)
            return results
    except Exception as e:
        print(f"Database error in select_list: {e}")
        raise e

def select_one(sql: str, params=None):
    params = params or {}
    cfg = current_app.config['db_config']

    try:
        with DBContextManager(cfg) as cur:
            cur.execute(sql, params)
            columns = [desc[0] for desc in cur.description]
            row = cur.fetchone()

            if row:
                row_dict = {}
                for i, col in enumerate(columns):
                    row_dict[col] = row[i]
                return row_dict
            return None
    except Exception as e:
        print(f"Database error in select_one: {e}")
        raise e
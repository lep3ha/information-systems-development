from database_clone.DBcm import DBContextManager
from flask import current_app

def select_list(_sql, user_list):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            cursor.execute(_sql, user_list)
            result = cursor.fetchall()
            schema = []
            for item in cursor.description:
                schema.append(item[0])
    return result, schema


def select_dict(_sql, user_dict):
    user_list = list(user_dict.values())
    result, schema = select_list(_sql, user_list)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    return result_dict


def execute_insert(_sql, user_dict: dict):
    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Курсор не создан')
        else:
            user_dict = list(user_dict.values())
            cursor.execute(_sql, user_dict)
            if cursor.rowcount == 0:
                raise ValueError('Insert не выполнен')
            last_inserted = cursor.fetchone()[0]
        return last_inserted
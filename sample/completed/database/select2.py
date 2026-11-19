from flask import current_app
from .DBcm import DBContextManager


def select_list(_sql, params=None):
    """
    Выполняет SQL запрос и возвращает результат в виде списка кортежей и схему колонок

    Args:
        _sql (str): SQL запрос
        params (list|tuple): Параметры для запроса

    Returns:
        tuple: (результат запроса, список названий колонок)
    """
    if params is None:
        params = []

    with DBContextManager(current_app.config['db_config']) as cursor:
        if cursor is None:
            raise ValueError('Database connection error')

        cursor.execute(_sql, params)
        result = cursor.fetchall()

        # Получаем названия колонок из описания курсора
        schema = []
        for item in cursor.description:
            schema.append(item[0])

        print(f"Schema: {schema}")
        print(f"Result: {result}")

    return result, schema


def select_dict(_sql, params=None):
    """
    Выполняет SQL запрос и возвращает результат в виде списка словарей

    Args:
        _sql (str): SQL запрос
        params (dict|list): Параметры для запроса

    Returns:
        list: Список словарей, где ключи - названия колонок
    """
    if params is None:
        params = {}

    # Преобразуем параметры в список, если передан словарь
    if isinstance(params, dict):
        param_list = []
        for key in params:
            param_list.append(params[key])
        print(f'Params converted to list: {param_list}')
    else:
        param_list = params

    # Выполняем запрос через select_list
    result, schema = select_list(_sql, param_list)

    # Преобразуем результат в список словарей
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))

    print(f"Result as dict: {result_dict}")
    return result_dict


def select_one_dict(_sql, params=None):
    """
    Выполняет SQL запрос и возвращает первую строку в виде словаря

    Args:
        _sql (str): SQL запрос
        params (dict|list): Параметры для запроса

    Returns:
        dict: Словарь с первой строкой результата или None
    """
    result = select_dict(_sql, params)
    return result[0] if result else None
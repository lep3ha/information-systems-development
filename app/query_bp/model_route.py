from dataclasses import dataclass
from datetime import date

from flask import current_app
from psycopg2 import Error

from app.db.select import select_list


QUERIES = {
    "products": {
        "title": "Товары выбранной категории",
        "template": "products.html",
        "sql": "products.sql",
        "columns": (("id", "Код товара"), ("name", "Товар"), ("category", "Категория")),
    },
    "suppliers": {
        "title": "Поставщики из выбранного города",
        "template": "suppliers.html",
        "sql": "suppliers.sql",
        "columns": (
            ("company_name", "Поставщик"), ("city", "Город"), ("phone", "Телефон"),
        ),
    },
    "deliveries": {
        "title": "Поставки поставщика за период",
        "template": "deliveries.html",
        "sql": "deliveries.sql",
        "columns": (
            ("id", "Номер поставки"), ("delivered_at", "Дата поставки (Москва)"),
            ("company_name", "Поставщик"), ("total", "Сумма поставки"),
        ),
    },
}


@dataclass
class ResultInfo:
    result: list
    status: bool
    err_message: str = ""
    status_code: int = 200


def positive_id(value):
    try:
        number = int(value)
    except ValueError:
        raise ValueError("Код должен быть целым положительным числом.") from None
    if not 1 <= number <= 2147483647:
        raise ValueError("Код должен быть от 1 до 2147483647.")
    return number


def query_params(query_name, values):
    if query_name == "products":
        return {"category_id": positive_id(values.get("category_id", ""))}
    if query_name == "suppliers":
        city = values.get("city", "").strip()
        if not city or len(city) > 100:
            raise ValueError("Введите город длиной от 1 до 100 символов.")
        if "\x00" in city:
            raise ValueError("Название города содержит недопустимый символ.")
        return {"city": city}

    supplier_id = positive_id(values.get("supplier_id", ""))
    try:
        start_date = date.fromisoformat(values.get("start_date", ""))
        end_date = date.fromisoformat(values.get("end_date", ""))
    except ValueError:
        raise ValueError("Введите начальную и конечную даты в формате ГГГГ-ММ-ДД.") from None
    if start_date > end_date:
        raise ValueError("Начальная дата не должна быть позже конечной.")
    return {"supplier_id": supplier_id, "start_date": start_date, "end_date": end_date}


def model_route(provider, query_name, values):
    try:
        params = query_params(query_name, values)
    except ValueError as error:
        return ResultInfo([], False, str(error), 400)

    if "db_config" not in current_app.config:
        current_app.logger.error("Не загружен файл app/data/db_config.json")
        return ResultInfo([], False, "База данных недоступна. Попробуйте позже.", 503)
    try:
        rows = select_list(provider.get(QUERIES[query_name]["sql"]), params)
    except Error:
        current_app.logger.exception("Ошибка выполнения запроса %s", query_name)
        return ResultInfo([], False, "База данных недоступна. Попробуйте позже.", 503)
    return ResultInfo(rows, True)

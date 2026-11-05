# Супермаркет — лабораторные работы по дисциплине «Разработка информационных систем»

Приложение на Flask с локальной PostgreSQL. Зависимости перечислены в `requirements.txt`.

- [Отчёт лабораторной работы № 1](docs/course/lab1/report.md).
- [Отчёт лабораторной работы № 2: авторизация, запуск и проверки](docs/course/lab2/report.md).

Параметры подключения разместить в `app/data/db_config.json` по примеру `app/data/db_config.example.json`. Для новой БД последовательно выполнить `app/db/db_data/tables.sql`, `input_data.sql` и `auth.sql`. Для существующей БД первой лабораторной выполнить только `auth.sql`.

Учебная учётная запись: логин `admin`, пароль `admin`.

```sh
python -m flask --app app.main_menu run
```

```sh
python -m unittest discover -v
```

Для интеграционных тестов задать `LAB1_TEST_DB_CONFIG` — путь к JSON-конфигурации доступной PostgreSQL. Тесты создают и удаляют собственную временную схему.

Учебная учётная запись кассира: `cashier` / `cashier`. Доступ к запросам запрещён.

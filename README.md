# Магазин — локальная разработка
Лабораторные работы по дисциплине "Разработка Информационных Систем"

Короткая инструкция по запуску проекта локально и через Docker.

Требования
- Python 3.11
- PostgreSQL (локально или в Docker)

Переменные окружения
Проект ожидает переменные для подключения к PostgreSQL:

- `POSTGRES_HOST` — хост БД
- `POSTGRES_PORT` — порт (обычно 5432 или 5440)
- `POSTGRES_DB` — имя базы данных (например, `market`)
- `POSTGRES_USER` — пользователь БД
- `POSTGRES_PASSWORD` — пароль

Файл `app/db/.env` содержит пример значений (в репозитории). Не храните секреты в публичных репозиториях.

Локальный запуск (без Docker)
1. Создайте виртуальное окружение и активируйте его:

```bash
python -m venv venv
source venv/bin/activate
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Экспортируйте переменные окружения (пример):

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5440
export POSTGRES_DB=market
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=968489
```

4. Инициализируйте схему и тестовые данные (psql должен быть доступен):

```bash
psql "host=$POSTGRES_HOST port=$POSTGRES_PORT dbname=$POSTGRES_DB user=$POSTGRES_USER" -f app/db/db_data/tables.sql
psql "host=$POSTGRES_HOST port=$POSTGRES_PORT dbname=$POSTGRES_DB user=$POSTGRES_USER" -f app/db/db_data/triggers.sql
psql "host=$POSTGRES_HOST port=$POSTGRES_PORT dbname=$POSTGRES_DB user=$POSTGRES_USER" -f app/db/db_data/input_data.sql
psql "host=$POSTGRES_HOST port=$POSTGRES_PORT dbname=$POSTGRES_DB user=$POSTGRES_USER" -f app/db/db_data/reports.sql
```

5. Запустите приложение:

```bash
python run.py
```

Запуск через Docker

Если вы запускаете Postgres отдельно (на хосте) — `docker-compose.yml` настроен так, чтобы брать `POSTGRES_*` из `app/db/.env` и использовать `host.docker.internal` для доступа к хосту из контейнера на macOS.

Запуск веб-контейнера:

```bash
docker compose up --build
```

Если хотите, чтобы БД запускалась в том же `docker-compose`, можно добавить сервис `db` в `docker-compose.yml` (я могу сделать это по запросу).

Тестирование и отладка
- Логи web через `docker compose logs -f web` или `python run.py` в виртуальном окружении.
- В .vscode/settings.json лежат настройки подключения к БД для удобства.

Контакты и правки
Если нужно — добавлю сервис `db` в compose, или помогу запустить миграции и проверить работу триггеров.

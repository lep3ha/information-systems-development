FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY tests ./tests
COPY docker/db_config.json ./app/data/db_config.json

EXPOSE 5000

CMD ["python", "-m", "flask", "--app", "app.main_menu", "run", "--host=0.0.0.0", "--port=5000"]

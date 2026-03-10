import psycopg2
from psycopg2 import sql, OperationalError
from dotenv import load_dotenv
import os

class DBContextManager:
    def __init__(self):
        load_dotenv()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        try:
            self.connection = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                dbname=os.getenv("POSTGRES_DB"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD")
            )
            self.cursor = self.connection.cursor()
            return self.cursor
        except OperationalError as e:
            print(f"[DB ERROR] Ошибка подключения к БД: {e}")
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.connection.rollback()
            print(f"[DB ROLLBACK] Ошибка: {exc_val}")
        else:
            self.connection.commit()
            print("[DB COMMIT] Изменения сохранены.")

        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

        return False

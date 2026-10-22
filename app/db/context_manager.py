from psycopg2 import connect

class DBContextManager:
    def __init__(self, db_config):
        self.db_config = db_config
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = connect(**self.db_config)
        try:
            self.cursor = self.connection.cursor()
        except Exception:
            try:
                self.connection.rollback()
            finally:
                self.connection.close()
            raise
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                self.connection.rollback()
            else:
                try:
                    self.connection.commit()
                except Exception:
                    self.connection.rollback()
                    raise
        finally:
            try:
                if self.cursor is not None:
                    self.cursor.close()
            finally:
                self.connection.close()
        return False

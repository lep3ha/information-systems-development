import pymysql

class DBContextManager:
    def __init__(self, config: dict):
        self.config = config
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = pymysql.connect(
            host=self.config['host'],
            user=self.config['user'],
            password=self.config['password'],
            database=self.config['database'],
            autocommit=False,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.Cursor
        )
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc, tb):
        try:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
        finally:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        return False
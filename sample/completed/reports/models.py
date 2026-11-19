from database.select import select_list, select_one
from database.DBcm import DBContextManager
from database.sql_provider import SQLProvider
from flask import current_app


class ReportsModel:
    def __init__(self):
        self.sql_provider = SQLProvider('SQL/reports')

    def check_report_exists(self, month, year):
        """Проверяет существование отчета за указанный период"""
        try:
            sql = self.sql_provider.get('check_report_exists.sql')
            result = select_one(sql, [month, year])
            return result['count'] > 0 if result else False
        except Exception as e:
            print(f"Ошибка при проверке отчета: {e}")
            return False

    def create_report(self, month, year):
        """Создает отчет используя хранимую процедуру через SQL-файл"""
        try:
            cfg = current_app.config['db_config']
            sql = self.sql_provider.get('create_report.sql')

            with DBContextManager(cfg) as cur:
                cur.execute(sql, (month, year))

            print(f"Детализированный отчет за {month}/{year} создан через процедуру")
            return True

        except Exception as e:
            print(f"Ошибка при создании отчета: {e}")
            import traceback
            traceback.print_exc()
            return False

    def get_reports_list(self):
        """Получает список всех отчетов (даты)"""
        sql = self.sql_provider.get('list_reports.sql')
        return select_list(sql)

    def get_report_by_date(self, month, year):
        """Получает детали отчета по дате"""
        sql = self.sql_provider.get('get_report_by_date.sql')
        return select_list(sql, [month, year])


reports_model = ReportsModel()
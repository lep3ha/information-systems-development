from app.db.context_manager import DBContextManager
from app.db.sql_provider import SQLProvider


class AnalyticsModel:
    def __init__(self):
        self.sql_provider = SQLProvider('app/analytics/sql')

    def list_sales_reports(self):
        try:
            with DBContextManager() as db:
                db.execute(self.sql_provider.get('select_sales_reports.sql'))
                rows = db.fetchall()
                cols = [d[0] for d in db.description]
                data = [dict(zip(cols, r)) for r in rows]
                return {'status': True, 'data': data}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': []}

    def list_purchase_reports(self):
        try:
            with DBContextManager() as db:
                db.execute(self.sql_provider.get('select_purchase_reports.sql'))
                rows = db.fetchall()
                cols = [d[0] for d in db.description]
                data = [dict(zip(cols, r)) for r in rows]
                return {'status': True, 'data': data}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': []}

    def get_sales_report_rows(self, report_id):
        try:
            sql = self.sql_provider.get('select_sales_report_rows.sql')
            with DBContextManager() as db:
                db.execute(sql, (report_id,))
                rows = db.fetchall()
                cols = [d[0] for d in db.description]
                data = [dict(zip(cols, r)) for r in rows]
                return {'status': True, 'data': data}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': []}

    def get_purchase_report_rows(self, report_id):
        try:
            sql = self.sql_provider.get('select_purchase_report_rows.sql')
            with DBContextManager() as db:
                db.execute(sql, (report_id,))
                rows = db.fetchall()
                cols = [d[0] for d in db.description]
                data = [dict(zip(cols, r)) for r in rows]
                return {'status': True, 'data': data}
        except Exception as e:
            return {'status': False, 'msg': str(e), 'data': []}

    def create_sales_report(self, month, year, creator_id):
        try:
            sql = self.sql_provider.get('create_sales_report_call.sql')
            with DBContextManager() as db:
                db.execute(sql, (month, year, creator_id))
                row = db.fetchone()
                return {'status': True, 'data': {'report_id': row[0] if row else None}}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

    def create_purchase_report(self, month, year, creator_id):
        try:
            sql = self.sql_provider.get('create_purchase_report_call.sql')
            with DBContextManager() as db:
                db.execute(sql, (month, year, creator_id))
                row = db.fetchone()
                return {'status': True, 'data': {'report_id': row[0] if row else None}}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

    def delete_sales_report(self, report_id):
        try:
            sql = self.sql_provider.get('delete_sales_report.sql')
            with DBContextManager() as db:
                db.execute(sql, (report_id, report_id))
                return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

    def delete_purchase_report(self, report_id):
        try:
            sql = self.sql_provider.get('delete_purchase_report.sql')
            with DBContextManager() as db:
                db.execute(sql, (report_id, report_id))
                return {'status': True}
        except Exception as e:
            return {'status': False, 'msg': str(e)}

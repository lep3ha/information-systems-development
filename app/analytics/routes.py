from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.analytics.model import AnalyticsModel
from app.analytics.forms import ReportCreateForm
from app.auth.access import permission_required
from app.db.context_manager import DBContextManager


analytics = Blueprint('analytics', __name__, template_folder='templates')
model = AnalyticsModel()

@analytics.route('/')
@permission_required('reports_viewer', 'reports_creator', 'reports_editor')
def index():
    sales = model.list_sales_reports()
    purchases = model.list_purchase_reports()
    return render_template('analytics/index.html', sales=sales['data'] if sales['status'] else [], purchases=purchases['data'] if purchases['status'] else [])


@analytics.route('/sales/<int:report_id>')
@permission_required('reports_viewer', 'reports_creator', 'reports_editor')
def view_sales(report_id):
    rows = model.get_sales_report_rows(report_id)
    if not rows['status']:
        flash(rows.get('msg', 'Ошибка получения отчёта'), 'danger')
        return redirect(url_for('analytics.index'))
    return render_template('analytics/view_sales.html', rows=rows['data'], report_id=report_id)


@analytics.route('/purchases/<int:report_id>')
@permission_required('reports_viewer', 'reports_creator', 'reports_editor')
def view_purchases(report_id):
    rows = model.get_purchase_report_rows(report_id)
    if not rows['status']:
        flash(rows.get('msg', 'Ошибка получения отчёта'), 'danger')
        return redirect(url_for('analytics.index'))
    return render_template('analytics/view_purchases.html', rows=rows['data'], report_id=report_id)


@analytics.route('/create_sales', methods=['GET', 'POST'])
@permission_required('reports_creator', 'reports_editor')
def create_sales():
    form = ReportCreateForm()
    if form.validate_on_submit():
        res = model.create_sales_report(form.month.data, form.year.data, session.get('user_id'))
        if res['status']:
            flash('Отчёт о продажах создан', 'success')
            return redirect(url_for('analytics.view_sales', report_id=res['data']['report_id']))
        flash(res.get('msg', 'Ошибка создания отчёта'), 'danger')
    return render_template('analytics/create_sales.html', form=form)


@analytics.route('/create_purchases', methods=['GET', 'POST'])
@permission_required('reports_creator', 'reports_editor')
def create_purchases():
    form = ReportCreateForm()
    if form.validate_on_submit():
        res = model.create_purchase_report(form.month.data, form.year.data, session.get('user_id'))
        if res['status']:
            flash('Отчёт о поставках создан', 'success')
            return redirect(url_for('analytics.view_purchases', report_id=res['data']['report_id']))
        flash(res.get('msg', 'Ошибка создания отчёта'), 'danger')
    return render_template('analytics/create_purchases.html', form=form)


@analytics.route('/delete_sales/<int:report_id>', methods=['POST'])
@permission_required('reports_creator', 'reports_editor')
def delete_sales(report_id):
    res = model.delete_sales_report(report_id)
    if res['status']:
        flash('Отчёт удалён', 'info')
    else:
        flash(res.get('msg', 'Ошибка удаления'), 'danger')
    return redirect(url_for('analytics.index'))


@analytics.route('/delete_purchases/<int:report_id>', methods=['POST'])
@permission_required('reports_creator', 'reports_editor')
def delete_purchases(report_id):
    res = model.delete_purchase_report(report_id)
    if res['status']:
        flash('Отчёт удалён', 'info')
    else:
        flash(res.get('msg', 'Ошибка удаления'), 'danger')
    return redirect(url_for('analytics.index'))

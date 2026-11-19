from flask import Blueprint, render_template, request, flash
from auth.access import login_required, group_required
from .models import reports_model

reports_bp = Blueprint('reports', __name__, template_folder='templates')


@reports_bp.route('/', methods=['GET'])
@login_required
def reports_menu():
    """Главное меню отчетов"""
    return render_template('reports_menu.html')


@reports_bp.route('/date_report', methods=['GET', 'POST'])
@login_required
@group_required
def date_report():
    """Отчет по дате - создание и просмотр"""
    if request.method == 'GET':
        return render_template('date_report.html')

    month = request.form.get('month')
    year = request.form.get('year')
    action = request.form.get('action')  # 'create' или 'view'

    if not month or not year:
        flash('Введите месяц и год')
        return render_template('date_report.html')

    try:
        month_int = int(month)
        year_int = int(year)

        if month_int < 1 or month_int > 12:
            flash('Месяц должен быть от 1 до 12')
            return render_template('date_report.html')

        if year_int < 2020 or year_int > 2030:
            flash('Год должен быть от 2020 до 2030')
            return render_template('date_report.html')

        # Проверяем существование отчета
        report_exists = reports_model.check_report_exists(month_int, year_int)

        if action == 'create':
            if report_exists:
                flash(f'Отчет за {month_int}/{year_int} уже был создан ранее')
            else:
                # Создаем новый отчет
                if reports_model.create_report(month_int, year_int):
                    flash(f'Отчет за {month_int}/{year_int} успешно создан!')
                else:
                    flash('Ошибка при создании отчета')

        elif action == 'view':
            if report_exists:
                # Получаем данные отчета
                report_data = reports_model.get_report_by_date(month_int, year_int)
                if report_data:
                    return render_template('report_results.html',
                                           report_data=report_data,
                                           month=month_int,
                                           year=year_int)
                else:
                    flash('Ошибка при загрузке отчета')
            else:
                flash(f'Отчет за {month_int}/{year_int} еще не создан')

    except ValueError:
        flash('Введите корректные числовые значения')
    except Exception as e:
        flash(f'Ошибка: {str(e)}')

    return render_template('date_report.html')
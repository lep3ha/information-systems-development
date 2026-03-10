# forms.py
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, DecimalField, DateField, IntegerField
from wtforms.validators import Optional, NumberRange

class CatalogFilterForm(FlaskForm):
    category = SelectField("Категория", choices=[("", "Все")], validators=[Optional()])
    min_price = DecimalField("Мин. цена", 
                           validators=[Optional(), NumberRange(min=0, message="Цена не может быть отрицательной")],
                           places=2)
    max_price = DecimalField("Макс. цена", 
                           validators=[Optional(), NumberRange(min=0, message="Цена не может быть отрицательной")],
                           places=2)
    sort_by = SelectField("Сортировка", choices=[
        ("name_asc", "Название ↑"),
        ("name_desc", "Название ↓"),
        ("price_asc", "Цена ↑"),
        ("price_desc", "Цена ↓")
    ])
    submit = SubmitField("Применить фильтры")

class SuppliersFilterForm(FlaskForm):
    city = SelectField("Город", choices=[("", "Все")], validators=[Optional()])
    min_contract_date = DateField("Дата контракта от", 
                                 format='%Y-%m-%d',
                                 validators=[Optional()])
    max_contract_date = DateField("Дата контракта до", 
                                 format='%Y-%m-%d',
                                 validators=[Optional()])
    sort_by = SelectField("Сортировка", choices=[
        ("name_asc", "Название ↑"),
        ("name_desc", "Название ↓"),
        ("city_asc", "Город ↑"),
        ("city_desc", "Город ↓"),
        ("date_asc", "Дата контракта ↑"),
        ("date_desc", "Дата контракта ↓"),
        ("invoice_count_asc", "Количество накладных ↑"),
        ("invoice_count_desc", "Количество накладных ↓"),
        ("total_invoices_asc", "Сумма накладных ↑"),
        ("total_invoices_desc", "Сумма накладных ↓")
    ])
    submit = SubmitField("Применить фильтры")

class InvoicesFilterForm(FlaskForm):
    supplier_id = SelectField("Поставщик", choices=[(0, "Все")], validators=[Optional()])
    min_delivery_date = DateField("Дата поставки от", 
                                 format='%Y-%m-%d',
                                 validators=[Optional()])
    max_delivery_date = DateField("Дата поставки до", 
                                 format='%Y-%m-%d',
                                 validators=[Optional()])
    min_total_cost = DecimalField("Сумма от", 
                                 validators=[Optional(), NumberRange(min=0)],
                                 places=2)
    max_total_cost = DecimalField("Сумма до", 
                                 validators=[Optional(), NumberRange(min=0)],
                                 places=2)
    sort_by = SelectField("Сортировка", choices=[
        ("date_asc", "Дата поставки ↑"),
        ("date_desc", "Дата поставки ↓"),
        ("cost_asc", "Сумма ↑"),
        ("cost_desc", "Сумма ↓"),
        ("supplier_asc", "Поставщик ↑"),
        ("supplier_desc", "Поставщик ↓")
    ])
    submit = SubmitField("Применить фильтры")
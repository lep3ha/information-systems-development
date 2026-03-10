from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class ReportCreateForm(FlaskForm):
    month = IntegerField('Месяц', validators=[DataRequired(), NumberRange(min=1, max=12)])
    year = IntegerField('Год', validators=[DataRequired(), NumberRange(min=2000, max=2100)])
    submit = SubmitField('Создать отчёт')

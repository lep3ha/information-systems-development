from flask_wtf import FlaskForm
from wtforms import HiddenField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class UpdateCartItemForm(FlaskForm):
    item_id = HiddenField('item_id', validators=[DataRequired()])
    quantity = IntegerField('quantity', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Обновить')

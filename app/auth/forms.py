from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(3, 25)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(5, 50)])
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(3, 25)])
    first_name = StringField('Имя', validators=[DataRequired(), Length(1, 50)])
    second_name = StringField('Фамилия', validators=[DataRequired(), Length(1, 50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(5, 50)])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')
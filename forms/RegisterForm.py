from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField, FloatField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    surname = StringField('фамилия пользователя', validators=[DataRequired()])
    age = IntegerField('возраст пользователя', validators=[DataRequired()])
    cost = FloatField('Ставка за час', validators=[DataRequired()])
    specialization = StringField('Ученик или Репетитор', validators=[DataRequired()])
    address = StringField('адресс пользователя', validators=[DataRequired()])
    submit = SubmitField('Войти')
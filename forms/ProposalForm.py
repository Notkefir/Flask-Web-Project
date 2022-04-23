from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, IntegerField, BooleanField, FloatField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class ProposalForm(FlaskForm):
    title = StringField('Тема', validators=[DataRequired()])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    #duration = StringField('Продолжительность', validators=[DataRequired()])
    coast = FloatField('цена', validators=[DataRequired()])
    submit = SubmitField('Submit')
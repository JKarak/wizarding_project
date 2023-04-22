from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired


class Login(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class Register(FlaskForm):
    name = StringField('Ник', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    submit = SubmitField('Войти')


class FindSpells(FlaskForm):
    keywords = StringField('Введите название', validators=[DataRequired()])
    type = SelectField('Choose month',choices=['Spells', 'Potions'])
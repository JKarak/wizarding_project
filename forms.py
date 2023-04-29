from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, SubmitField, EmailField, FileField, SelectField)
from wtforms.validators import DataRequired


class Login(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class Register(FlaskForm):
    name = StringField('Nickname', validators=[DataRequired()])
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    avatar = FileField('Select avatar')
    submit = SubmitField('Register')


class FindSpells(FlaskForm):
    keywords = StringField('Type keywords', validators=[DataRequired()])
    category = SelectField('Choose type', choices=['Spells', 'Potions'])
    submit = SubmitField('Search')

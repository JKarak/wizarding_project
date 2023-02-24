from flask import Flask
from flask import render_template, redirect
from forms import LoginForm, RegForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def a():
    return "Миссия Колонизация Марса"


@app.route('/index')
def index():
    return "И на Марсе будут яблони цвести!"


@app.route('/sign')
def sign():
    form = LoginForm()
    formR = RegForm()
    return render_template('sign_form.html', title='Авторизация', form=form, formR=formR)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

from flask import Flask, render_template, redirect
from forms import LoginIn
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def loginIn():
    form = LoginIn()
    wrong_password = ' '
    if form.validate_on_submit():
        req = 'http://jusrager.pythonanywhere.com/api/v1/user/auth'
        response = requests.get(req)
        if response:
            return redirect('/main')
        else:
            wrong_password = 'Неправильный пароль'
    return render_template('page-sign-up.html', form=form, wrong_password=wrong_password)


@app.route('/')
def main():
    pass


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

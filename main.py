from flask import Flask, render_template, redirect, session
from forms import Login, Register, FindSpells
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

# вход
@app.route('/login')
def signIn():
    form = Login()
    wrong_password = ' '
    if form.validate_on_submit():
        data = {
            "login": form.login.data,
            "password": form.password.data
        }

        req = 'http://jusrager.pythonanywhere.com/api/v1/user/registration'
        response = requests.post(req, json=data)

        if response:
            session['username'] = data['login']
            return redirect('/main')
        else:
            wrong_password = 'Неправильное имя пользователя, логин или пароль'
    return render_template('page-sign-in.html', form=form, wrong_password=wrong_password)

# регистрация
@app.route('/register')
def signUp():
    form = Register()
    wrong_password = ' '
    if form.validate_on_submit():
        data = {
            "name": form.name.data,
            "login": form.login.data,
            "password": form.password.data,
            "email": form.email.data
        }

        req = 'http://jusrager.pythonanywhere.com/api/v1/user/auth'
        response = requests.post(req, json=data)

        if response:
            return redirect('/main')
        else:
            wrong_password = 'Неправильное имя пользователя, логин или пароль'
    return render_template('page-sign-up.html', form=form, wrong_password=wrong_password)


# основная страница
@app.route('/')
def main():
    print(session.get('username'))
    form = FindSpells()
    req = 'https://wizard-world-api.herokuapp.com/Spells'
    find = requests.get(req, params={'name': ''})

    '''req2 = f'http://jusrager.pythonanywhere.com/api/v1/user/{login}/favourite/spells'
    favourites = requests.get(req2)

    effects = []

    for spell in favourites.json()['spells']:
        req = 'https://wizard-world-api.herokuapp.com/Spells'
        spell = requests.get(req, params={'name': spell['name']}).json()
        effects.append(spell['effect'])'''
    params = {'form': form,
              'effect': 'a'}
    return render_template('index-3.html', form=params['form'], effects='0')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

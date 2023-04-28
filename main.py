from flask import Flask, render_template, redirect, session, request, url_for
from forms import Login, Register, FindSpells
import datetime
import requests

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)


@app.route('/login', methods=["GET", "POST"])
def signIn():
    user = session.get("usename", 0)

    if user:
        return redirect('/')
    else:
        form = Login()
        wrong_password = ' '

        if form.validate_on_submit():
            data = {
                "login": form.login.data,
                "password": form.password.data
            }

            req = 'http://jusrager.pythonanywhere.com/user/auth'
            resp = requests.post(req, json=data)
            print(resp.url)

            if resp:
                session['username'] = data['login']
                return redirect('/')
            else:
                wrong_password = 'Неправильное имя пользователя, логин или пароль'
        return render_template('login.html', form=form, wrong_password=wrong_password)


@app.route('/register', methods=["GET", "POST"])
def signUp():
    user = session.get("usename", 0)

    if user:
        return redirect('/')
    else:
        form = Register()
        wrong_password = ' '

        if form.validate_on_submit():
            data = {
                "name": form.name.data,
                "login": form.login.data,
                "password": form.password.data,
                "email": form.email.data
            }

            req = 'http://jusrager.pythonanywhere.com/user/registration'
            try:
                response = requests.post(req, data=data, timeout=1.5)
                print(response)
                if response:
                    session['username'] = data['login']
                    return redirect('/')
                else:
                    wrong_password = 'Неправильное имя пользователя, логин или пароль'
            except requests.Timeout:
                wrong_password = 'Сервер регистрации не доступен'

        return render_template('register.html', form=form, wrong_password=wrong_password)


# основная страница
@app.route('/', methods=["GET", "POST"])
def main():
    user = session.get("usename", 0)
    if True:
        form = FindSpells()
        if form.validate_on_submit():
            params = {'keywords': form.keywords.data,
                      'category': form.category.data}

            return redirect(url_for('search', **params))

        req = 'https://wizard-world-api.herokuapp.com/Spells'
        find = requests.get(req, params={'name': ''})

        '''req2 = f'http://jusrager.pythonanywhere.com/api/v1/user/{login}/favourite/spells'
        spells_favourite = requests.get(req2)
        spells_count_fav = spells_favourite.json()['spells']

        req3 = f'http://jusrager.pythonanywhere.com/api/v1/user/{login}/favourite/potions'
        potions_favourite = requests.get(req3)
        potions_count_fav = potions_favourite.json()['spells']'''

        effects = []
        titles = []
        ids = []
        page = []
        req = 'http://jusrager.pythonanywhere.com/api/v1/user/makaka/favourite/spells'
        spells = requests.get(req).json()[0:2]
        for spell in spells:
            page.append('spells')
            ids.append(spell['id'])
            titles.append(spell['name'])
            effects.append(spell['effect'])

        req = 'https://wizard-world-api.herokuapp.com/Elixirs'
        potions = requests.get(req).json()[0:2]
        for potion in potions:
            page.append('potions')
            ids.append(potion['id'])
            titles.append(potion['name'])
            effects.append(potion['effect'])

        params = {'form': form,
                  'effects': effects,
                  'titles': titles,
                  'ids': ids,
                  'page': page
                  }

        return render_template('index.html', **params)
    else:
        return redirect('/login')


@app.route('/spells/<id>')
def spells(id):
    # req = f''
    # data = requests.get(req)
    # info = data.json()

    info = {"id": id,
            "name": 1,
            "effect": 2,
            "sideEffects": 3,
            "characteristics": 4,
            "time": 5,
            "difficulty": 6,
            "ingredients": 7}

    params = {"id": id,
              "name": info['name'],
              "effect": info['effect'],
              "sideEffects": info['sideEffects'],
              "characteristics": info['characteristics'],
              "time": info['time'],
              "difficulty": info['difficulty'],
              "ingredients": info['ingredients']}

    return render_template('spells.html', **params)


@app.route('/potions/<id>')
def potions(id):
    # req = f''
    # data = requests.get(req)
    # info = data.json()

    info = {"id": id,
            "name": 1,
            "incantation": 2,
            "effect": 3,
            "canBeVerbal": 4,
            "type": 5,
            "light": 6,
            }

    params = {"id": id,
              "name": info['name'],
              "incantation": info['incantation'],
              "effect": info['effect'],
              "canBeVerbal": info['canBeVerbal'],
              "type": info['type'],
              "light": info['light'],
              }

    return render_template('potions.html', **params)


@app.route('/category/<type>')
def category(type):
    effects = []
    titles = []
    ids = []
    page = []
    req = 'https://wizard-world-api.herokuapp.com/Spells'
    spells = requests.get(req).json()[0:4]
    for spell in spells:
        page.append('spells')
        ids.append(spell['id'])
        titles.append(spell['name'])
        effects.append(spell['effect'])

    params = {'effects': effects,
              'titles': titles,
              'ids': ids,
              'page': page
              }
    return render_template('category.html', **params)


@app.route('/acc')
def acc():
    # req = 'https://wizard-world-api.herokuapp.com/Spells'
    # info = requests.get(req).json()

    info = {'name': 1,
            'number_of_favorites': 2}

    params = {'name': info['name'],
              'number_of_favorites': info['number_of_favorites']}

    return render_template('acc.html', **params)


@app.route('/search')
def search():
    # 'keywords': request.args['keywords'],
    # 'category': request.args['category'],
    effects = []
    titles = []
    ids = []
    page = []
    req = 'https://wizard-world-api.herokuapp.com/Spells'
    spells = requests.get(req).json()[0:2]
    for spell in spells:
        page.append('spells')
        ids.append(spell['id'])
        titles.append(spell['name'])
        effects.append(spell['effect'])

    params = {
        'effects': effects,
        'titles': titles,
        'ids': ids,
        'page': page
    }
    return render_template('search.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

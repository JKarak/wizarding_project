import datetime
import base64
import requests
from flask import (Flask, render_template, redirect, session, request, url_for, flash)
from forms import Login, Register, FindSpells


__WEB_API_URL = "http://127.0.0.1:5000"
__WEB_API_TIMEOUT = 10

__WIZARD_WORLD_API_URL = "https://wizard-world-api.herokuapp.com"
__WIZARD_WORLD_API_TIMEOUT = 20


app = Flask(__name__)
app.config["SECRET_KEY"] = "yandexlyceum_secret_key"
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(days=365)


@app.route("/login", methods=["GET", "POST"])
def sign_in():
    user = session.get("usename")
    if user:
        return redirect("/")

    form = Login()
    wrong_password = " "

    if form.validate_on_submit():
        data = {
            "login": form.login.data,
            "password": form.password.data
        }

        req = f"{__WEB_API_URL}/user/auth"
        response = requests.get(req, params=data, timeout=__WEB_API_TIMEOUT)
        if response:
            session["username"] = data["login"]
            return redirect("/")

        wrong_password = "Неправильное имя пользователя, логин или пароль"

    return render_template("login.html", form=form, wrong_password=wrong_password)


@app.route("/register", methods=["GET", "POST"])
def sign_up():
    user = session.get("usename")
    if user:
        return redirect("/")

    form = Register()
    if form.validate_on_submit():
        avatar_buffer = form.avatar.data.read()
        data = {
            "name": form.name.data,
            "login": form.login.data,
            "key": form.password.data,
            "email": form.email.data,
            "avatar": base64.b64encode(avatar_buffer).decode("utf-8"),
        }

        req = f"{__WEB_API_URL}/user/registration"
        try:
            response = requests.post(req, json=data, timeout=__WEB_API_TIMEOUT)
            if response:
                session["username"] = data["login"]
                return redirect("/")

            flash("Неправильное имя пользователя, логин или пароль", category='error')
        except requests.Timeout:
            flash("Сервер регистрации временно не доступен", category='error')

    return render_template("register.html", form=form)


@app.route("/", methods=["GET", "POST"])
def main():
    if "username" not in session:
        return redirect("/login")

    form = FindSpells()
    if form.validate_on_submit():
        params = {
            "keywords": form.keywords.data,
            "category": form.category.data
        }

        return redirect(url_for("search", **params))

    user = session["username"]

    effects = []
    titles = []
    ids = []
    page = []

    headers = {
        "Content-Type": "application/json"
    }

    req = f"{__WEB_API_URL}/user/{user}/favourite/spells"
    spells = requests.get(req, headers=headers, timeout=__WEB_API_TIMEOUT)
    if spells:
        for spell in spells.json():
            page.append("spells")
            ids.append(spell["id"])
            titles.append(spell["name"])
            effects.append(spell["effect"])
    else:
        req = f"{__WIZARD_WORLD_API_URL}/Spells"
        spells = requests.get(req, headers=headers, timeout=__WIZARD_WORLD_API_TIMEOUT)
        for spell in spells.json()[0:4]:
            page.append("spells")
            ids.append(spell["id"])
            titles.append(spell["name"])
            effects.append(spell["effect"])

    req = f"{__WEB_API_URL}/user/{user}/favourite/potions"
    potions = requests.get(req, headers=headers, timeout=__WEB_API_TIMEOUT)
    if potions:
        for potion in potions.json():
            page.append("potions")
            ids.append(potion["id"])
            titles.append(potion["name"])
            effects.append(potion["effect"])
    else:
        req = f"{__WIZARD_WORLD_API_URL}/Elixirs"
        potions = requests.get(req, headers=headers, timeout=__WIZARD_WORLD_API_TIMEOUT)
        for potion in potions.json()[0:4]:
            page.append("potions")
            ids.append(potion["id"])
            titles.append(potion["name"])
            effects.append(potion["effect"])

    params = {
        "form": form,
        "effects": effects,
        "titles": titles,
        "ids": ids,
        "page": page,
    }

    return render_template("index.html", **params)


@app.route("/spells/<string:id>")
def spells(id: str):
    if "username" not in session:
        return redirect("/login")

    headers = {
        "Content-Type": "application/json"
    }

    req = f"{__WEB_API_URL}/spells/{id}"
    response = requests.get(req, headers=headers, timeout=__WEB_API_TIMEOUT)
    if response:
        spell = response.json()
        params = {
            'id': spell['uuid'],
            'name': spell['name'],
            'incantation': spell['incantation'],
            'effect': spell['effect'],
            'canBeVerbal': spell['canBeVerbal'],
            'type': spell['type'],
            'light': spell['light']
        }
        # 'picture': spell['picture']

        return render_template("spells.html", **params)

    req = f"{__WIZARD_WORLD_API_URL}/Spells/{id}"
    response = requests.get(req, headers=headers, timeout=__WIZARD_WORLD_API_TIMEOUT)
    if response:
        spell = response.json()
        params = {
            'id': spell['id'],
            'name': spell['name'],
            'incantation': spell['incantation'],
            'effect': spell['effect'],
            'canBeVerbal': spell['canBeVerbal'],
            'type': spell['type'],
            'light': spell['light'],
            'creator': spell['creator']
        }

        return render_template("spells.html", **params)

    flash('The requested spell was not found!', category='error')
    return redirect('/')


@app.route("/potions/<string:id>")
def potions(id: str):
    if "username" not in session:
        return redirect("/login")

        # potion
        # qu = {'uuid': pt.uuid, 'name': pt.name, 'effect': pt.effect,
        #       'sideEffects': pt.sideEffects, 'characteristics': pt.characteristics, 'time': pt.time,
        #       'difficulty': pt.difficulty, 'ingredients': pt.ingredients, 'inventors': pt.inventors,
        #       'manufacturer': pt.manufacturer, 'picture': pt.picture}


    headers = {
        "Content-Type": "application/json"
    }

    req = f"{__WEB_API_URL}/potions/{id}"
    response = requests.get(req, headers=headers, timeout=__WEB_API_TIMEOUT)
    if response:
        spell = response.json()
        params = {
            'id': spell['uuid'],
            'name': spell['name'],
            'effect': spell['effect'],
            'sideEffects': spell['sideEffects'],
            'characteristics': spell['characteristics'],
            'time': spell['time'],
            'difficulty': spell['difficulty'],
            'manufacturer': spell['manufacturer']
        }
        # 'picture': spell['picture']

        return render_template("potions.html", **params)

    req = f"{__WIZARD_WORLD_API_URL}/Elixirs/{id}"
    response = requests.get(req, headers=headers, timeout=__WIZARD_WORLD_API_TIMEOUT)
    if response:
        spell = response.json()
        params = {
            'id': spell['id'],
            'name': spell['name'],
            'effect': spell['effect'],
            'sideEffects': spell['sideEffects'],
            'characteristics': spell['characteristics'],
            'time': spell['time'],
            'difficulty': spell['difficulty'],
            'manufacturer': spell['manufacturer']
        }

        return render_template("potions.html", **params)

    flash('The requested potion was not found!', category='error')
    return redirect('/')


@app.route("/category/<string:spell_type>")
def category(spell_type: str):
    if "username" not in session:
        return redirect("/login")

    effects = []
    titles = []
    ids = []
    page = []
    len_spells = 0

    req = f"{__WEB_API_URL}/spellsbytype/{spell_type.capitalize()}"
    response = requests.get(req, timeout=__WEB_API_TIMEOUT)
    if response:
        spells = response.json()
        len_spells = len(spells)
        for spell in spells:
            page.append("spells")
            ids.append(spell["uuid"])
            titles.append(spell["name"])
            effects.append(spell["effect"])

    params = {
        "effects": effects,
        "titles": titles,
        "ids": ids,
        "page": page,
        "len_spells": len_spells,
    }

    return render_template("category.html", **params)


@app.route("/acc")
def acc():
    if "username" not in session:
        return redirect("/login")

    info = {
        "name": 1,
        "number_of_favorites": 2
    }

    params = {
        "name": info["name"],
        # 'avatar': avatar,
        "number_of_favorites": info["number_of_favorites"],
    }

    return render_template("acc.html", **params)


@app.route("/search")
def search():
    if "username" not in session:
        return redirect("/login")

    effects = []
    titles = []
    ids = []
    page = []
    len_spells = 0

    keywords = request.args.get("keywords")
    category = request.args.get("category")

    params = {
        "Name": keywords
    }
    req = f"{__WIZARD_WORLD_API_URL}/{category}"
    response = requests.get(req, params=params, timeout=__WIZARD_WORLD_API_TIMEOUT)
    if response:
        spells = response.json()
        len_spells = len(spells)
        for spell in spells:
            page.append("spells")
            ids.append(spell["id"])
            titles.append(spell["name"])
            effects.append(spell["effect"])

    params = {
        "effects": effects,
        "titles": titles,
        "ids": ids,
        "page": page,
        "len_spells": len_spells,
    }

    return render_template("search.html", **params)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

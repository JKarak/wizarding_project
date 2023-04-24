import random
import string
from email.header import Header

import db.data_base_create as data_base_create
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import datetime as dt
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import hashlib
import requests

class DataBaseManager():
    name = os.path.join('db', 'harry_potter_data.db')
    engine = create_engine(f"sqlite:///{name}")
    session = Session(bind=engine)

    @staticmethod
    def generate_random_password(wer):
        characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
        length = 8
        random.shuffle(characters)
        password = []
        for i in range(length):
            password.append(random.choice(characters))
        random.shuffle(password)
        new_password = "".join(password) + wer
        return new_password

    @staticmethod
    def add_user(login, key, email):
        date_create = dt.datetime.now().date()
        if DataBaseManager.is_okay(key):
            ash = login + key
            ash = hashlib.md5(ash.encode())
            ash = ash.hexdigest()
            user_1 = data_base_create.User(password_login_hash=ash, email=email, date_create=str(date_create))
            DataBaseManager.session.add(user_1)
            DataBaseManager.session.commit()
            return user_1.id
        else:
            return 0

    @staticmethod
    def add_avatar(email, file_path):
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.email == email).one()
        user.avatar_file = file_path
        DataBaseManager.session.commit()

    @staticmethod
    def entrance_user(login, key):
        ash = login + key
        ash = hashlib.md5(ash.encode())
        ash = ash.hexdigest()
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.password_login_hash == ash).all()
        if user:
            return user[0].id
        else:
            return 0


    @staticmethod
    def forgot_password(login, email):
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.email == email).all()
        if user:
            smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
            smtpObj.starttls()
            smtpObj.login("work_smtp_ofkate@mail.ru", "axH8vCX8ZzPBnqHaHuUF")
            wer = user.id
            password = wer.generate_random_password()
            m = f"""Ваш новый пароль: {password}\n. Вы сможете поменять его в любой момент. \n\n Не сообщайте никому эти данные в целях безопасности!"""
            subject = 'Новый пароль wizard_world'
            msg = MIMEText(m, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            smtpObj.sendmail("work_smtp_ofkate@mail.ru", email, msg.as_string())
            smtpObj.quit()
            ash_2 = login + password
            ash_2 = hashlib.md5(ash_2.encode())
            ash_2 = ash_2.hexdigest()
            user.password_login_hash = ash_2
            DataBaseManager.session.commit()
            return 'successfully change password'
        else:
            return 'wrong email'

    @staticmethod
    def change_password(login, email, old_password, new_password):
        ash = login + old_password
        ash = hashlib.md5(ash.encode())
        ash = ash.hexdigest()
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.email == email)
        if user.password_login_hash == ash:
            if DataBaseManager.is_okay(new_password):
                ash_2 = login + new_password
                ash_2 = hashlib.md5(ash_2.encode())
                ash_2 = ash_2.hexdigest()
                user.password_login_hash = ash_2
                DataBaseManager.session.commit()
                return 'successfully change password'
            else:
                return 'wrong format of password'
        else:
            return 'wrong password'

    @staticmethod
    def is_okay(key):
        if len(key) > 9 and not key.isalnum():
            return True
        return False

    @staticmethod
    def add_to_favourite_spell(uuid, user_id):
        date = dt.datetime.now().date()
        fs = data_base_create.FavouriteSpells(user_id=user_id, spell_uuid=uuid, active=1, date=str(date))
        DataBaseManager.session.add(fs)
        DataBaseManager.session.commit()

    @staticmethod
    def add_to_favourite_potion(uuid, user_id):
        date = dt.datetime.now().date()
        fp = data_base_create.FavouritePotions(user_id=user_id, potion_uuid=uuid, active=1, date=str(date))
        DataBaseManager.session.add(fp)
        DataBaseManager.session.commit()

    @staticmethod
    def all_favourite(user_id):
        fav_spells = DataBaseManager.session.query(data_base_create.FavouriteSpells).filter(
            data_base_create.FavouriteSpells.user_id == user_id).filter(
            data_base_create.FavouriteSpells.active == 1).all()
        fav_potions = DataBaseManager.session.query(data_base_create.FavouritePotions).filter(
            data_base_create.FavouritePotions.user_id == user_id).filter(
            data_base_create.FavouritePotions.active == 1).all()
        a = fav_potions + fav_spells
        a = sorted(a, key=lambda x: x.date)
        for i in range(len(a)):
            if isinstance(a[i], data_base_create.FavouriteSpells):
                a[i] = a[i].spell_uuid
            else:
                a[i] = a[i].potion_uuid
        return a

    @staticmethod
    def potions_favourite(user_id):
        a = DataBaseManager.session.query(data_base_create.FavouritePotions).filter(
            data_base_create.FavouritePotions.user_id == user_id).filter(
            data_base_create.FavouritePotions.active == 1).all()
        a = sorted(a, key=lambda x: x.date)
        for i in range(len(a)):
            a[i] = a[i].potion_uuid
        return a

    @staticmethod
    def spells_favourite(user_id):
        a = DataBaseManager.session.query(data_base_create.FavouriteSpells).filter(
            data_base_create.FavouriteSpells.user_id == user_id).filter(
            data_base_create.FavouriteSpells.active == 1).all()
        a = sorted(a, key=lambda x: x.date)
        for i in range(len(a)):
            a[i] = a[i].spell_uuid
        return a

    @staticmethod
    def get_user_info(email):
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.email == email).all()
        if user:
            user = user[0]
            js = {'id': user.id, 'name': user.name, 'email': user.email, 'avatar': user.avatar_file}
            return js
        else:
            return 0

    @staticmethod
    def get_random_types(num):
        all_types = DataBaseManager.session.query(data_base_create.User).all()
        random.shuffle(all_types)
        types = []
        for i in range(num):
            types.append((all_types[i].name_of_type, all_types[i].file))
        return types

    @staticmethod
    def add_to_viewed_potions(uuid, user_id):
        date = dt.datetime.now().date()
        fp = data_base_create.ViewedPotions(user_id=user_id, potion_uuid=uuid, date=str(date))
        DataBaseManager.session.add(fp)
        DataBaseManager.session.commit()

    @staticmethod
    def add_to_viewed_spells(uuid, user_id):
        date = dt.datetime.now().date()
        fp = data_base_create.ViewedSpells(user_id=user_id, spell_uuid=uuid, date=str(date))
        DataBaseManager.session.add(fp)
        DataBaseManager.session.commit()

    @staticmethod
    def find_spell(id):
        req = 'https://wizard-world-api.herokuapp.com/Spells'
        spells = requests.get(req).json()
        for spell in spells:
            if spell['id'] == id:
                return spell

    @staticmethod
    def find_potion(id):
        req = 'https://wizard-world-api.herokuapp.com/Elexirs'
        potions = requests.get(req).json()
        for potion in potions:
            if potion['id'] == id:
                return potion

    @staticmethod
    def add_potion(potion):
        ingr = ', '.join(list(map(lambda x: x['name'], potion['ingredients'])))
        inv = ', '.join(list(map(lambda x: x['firstName'] + ' ' + x['lastName'], potion['inventors'])))
        pt = data_base_create.Potions(uuid=potion['id'], neme=potion['name'], effect=potion['effect'], sideEffects=potion['sideEffects'],
                                      characteristics=potion['characteristics'], time=potion['time'], difficulty=potion['difficulty'],
                                      ingredients=ingr, inventors=inv, manufacturer=potion['manufacturer'])
        DataBaseManager.session.add(pt)
        DataBaseManager.session.commit()

    @staticmethod
    def add_spell(spell):
        pt = data_base_create.Potions(uuid=spell['id'], neme=spell['name'], incantation=spell['incantation'],
                                      effect=spell['effect'], canBeVerbal=spell['canBeVerbal'],
                                      type=spell['type'], light=spell['light'],
                                      creator=spell['creator'])
        DataBaseManager.session.add(pt)
        DataBaseManager.session.commit()

   ''' @staticmethod
    def get_potion(id):
        pt = DataBaseManager.session.query(data_base_create.Potions).filter(
            data_base_create.Potions.uuid == id).all()
        if pt:
            pt = pt[0]
            qu = {'id': pt.uuid, 'name': pt.name, 'effect': pt.effect,
                  'sideEffects': pt.sideEffects, 'characteristics': pt.characteristics, 'time': pt.time,
                  'difficulty': pt.difficulty, 'ingredients': pt.ingredients, 'inventors': pt.inventors,
                  'manufacturer': pt.manufacturer}
        else:
            id.find_potion()'''








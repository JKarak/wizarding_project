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
    def add_avatar(user_id, file_path):
        user = DataBaseManager.session.query(data_base_create.User).get(user_id)
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
            wer = login
            password = wer.generate_random_password()
            m = f"""Ваш новый пароль: {password}\n. Вы сможете поменять его в любой момент. \n\n Не сообщайте никому эти данные в целях безопасности!"""
            subject = 'Новый пароль wizard_world'
            msg = MIMEText(m, 'plain', 'utf-8')
            msg['Subject'] = Header(subject, 'utf-8')
            smtpObj.sendmail("work_smtp_ofkate@mail.ru", email, msg.as_string())
            smtpObj.quit()
        else:
            return 0
        pass

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
    def get_user_info(user):
        pass

    @staticmethod
    def get_random_types(num):
        pass
import db.data_base_create as data_base_create
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import datetime as dt
import os

class DataBaseManager():
    name = os.path.join('db', 'harry_potter_data.db')
    engine = create_engine(f"sqlite:///{name}")
    session = Session(bind=engine)

    @staticmethod
    def add_user(login, key, email):
        date_create = dt.datetime.now().date()
        if DataBaseManager.is_okay(key):
            user_1 = data_base_create.User(login=login, key=key, email=email, date_create=str(date_create))
            DataBaseManager.session.add(user_1)
            DataBaseManager.session.commit()
            return user_1.id
        else:
            return 'wrong format of password'

    @staticmethod
    def add_avatar(user_id, file_path):
        user = DataBaseManager.session.query(data_base_create.User).get(user_id)
        user.avatar_file = file_path
        DataBaseManager.session.commit()

    @staticmethod
    def forgot_password(user_id):
        user_email = DataBaseManager.session.query(data_base_create.User).get(user_id).email
        pass

    @staticmethod
    def change_password(user_id, old_password, new_password):
        user = DataBaseManager.session.query(data_base_create.User).get(user_id)
        if user.key == old_password:
            if DataBaseManager.is_okay(new_password):
                user.key = new_password
                DataBaseManager.session.commit()
                return 'successfully change password'
            else:
                return 'wrong format of password'
        else:
            return 'wrong password'

    @staticmethod
    def is_okay(key):
        if len(key) > 9 and not key.isdigit() and not key.isalpha():
            return True
        return False

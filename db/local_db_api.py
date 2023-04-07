import db.data_base_create as data_base_create
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import datetime as dt
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class DataBaseManager():
    name = os.path.join('db', 'harry_potter_data.db')
    engine = create_engine(f"sqlite:///{name}")
    session = Session(bind=engine)

    @staticmethod
    def add_user(login, key, email):
        date_create = dt.datetime.now().date()
        if DataBaseManager.is_okay(key):
            user_1 = data_base_create.User(login=login, password=key, email=email, date_create=str(date_create))
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
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.login == login).filter(
            data_base_create.User.password == key)
        if user:
            return user.id
        else:
            return 0


    @staticmethod
    def forgot_password(login, email):
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.login == login).filter(
            data_base_create.User.email == email)
        if user:
            # import necessary packages
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            import smtplib
            # create message object instance
            msg = MIMEMultipart()
            message = "Thank you"
            # setup the parameters of the message
            password = "your_password"
            msg['From'] = "your_address"
            msg['To'] = "to_address"
            msg['Subject'] = "Subscription"
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            # create server
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            # Login Credentials for sending the mail
            server.login(msg['From'], password)
            # send the message via the server.
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            print
            "successfully sent email to %s:" % (msg['To'])
        else:
            return 0
        pass

    @staticmethod
    def change_password(login, email, old_password, new_password):
        user = DataBaseManager.session.query(data_base_create.User).filter(
            data_base_create.User.login == login).filter(
            data_base_create.User.email == email)
        if user.password == old_password:
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
        if len(key) > 9 and not key.isalnum():
            return True
        return False

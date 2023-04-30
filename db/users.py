import hashlib

from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import db.data_base_create as data_base_create
import datetime as dt


if __name__ == '__main__':
    login = input()
    key = input()
    engine = create_engine("sqlite:///db/harry_potter_data.db")
    session = Session(bind=engine)
    ash = login + key
    ash = hashlib.md5(ash.encode())
    ash = ash.hexdigest()
    date_create = dt.datetime.now().date()
    user_1 = data_base_create.User(name='Катюшка', password_login_hash=ash,
                                   email='riabovakate@yandex.ru', date_create=str(date_create))
    session.add(user_1)
    session.commit()

import datetime as dt
import hashlib
from sqlalchemy import (create_engine, MetaData, Table, Integer,
                        String, Column, DateTime, ForeignKey, Numeric, SmallInteger)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship

from . import data_base_create


if __name__ == '__main__':
    login = input()
    key = input()
    engine = create_engine("sqlite:///data/harry_potter_data.db")
    session = Session(bind=engine)
    ash = login + key
    ash = hashlib.md5(ash.encode())
    ash = ash.hexdigest()
    date_create = dt.datetime.now().date()
    user_1 = data_base_create.User(name='Катюшка', password_login_hash=ash,
                                   email='riabovakate@yandex.ru', date_create=str(date_create))
    session.add(user_1)
    session.commit()

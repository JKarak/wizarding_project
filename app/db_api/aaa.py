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

from db_api import local_db_api

if __name__ == '__main__':
    a = local_db_api.DataBaseManager()
    print(a.potions_favourite(1))
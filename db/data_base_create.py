from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///harry_potter_data.db")

Base = declarative_base()

class User(Base):  # 1
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    login = Column(String(100), nullable=False)
    key = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    avatar_file = Column(String(200), default='0')
    date_create = Column(String(100), nullable=False)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
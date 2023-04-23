from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
engine = create_engine("sqlite:///harry_potter_data.db")

Base = declarative_base()

class User(Base):  # 1
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    password_login_hash = Column(String(128), nullable=False)
    email = Column(String(100), nullable=False)
    avatar_file = Column(String(200), default='0')
    date_create = Column(String(100), nullable=False)
    potions_rel_fav = relationship("FavouritePotions", back_populates="user_rel")
    potions_rel_view = relationship("ViewedPotions", back_populates="user_rel")
    spells_rel_fav = relationship("FavouriteSpells", back_populates="user_rel")
    spells_rel_view = relationship("ViewedSpells", back_populates="user_rel")

class FavouritePotions(Base):
    __tablename__ = 'favourite_potions'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    potion_uuid = Column(String(36))
    active = Column(Integer(), unique=False)
    date = Column(String(100), nullable=False)
    user_rel = relationship("User", back_populates="potions_rel_fav")


class ViewedPotions(Base):
    __tablename__ = 'viewed_potions'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    potion_uuid = Column(String(36))
    date = Column(String(100), nullable=False)
    user_rel = relationship("User", back_populates="potions_rel_view")

class FavouriteSpells(Base):
    __tablename__ = 'favourite_spells'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    spell_uuid = Column(String(36))
    active = Column(Integer(), unique=False)
    date = Column(String(100), nullable=False)
    user_rel = relationship("User", back_populates="spells_rel_fav")


class ViewedSpells(Base):
    __tablename__ = 'viewed_spells'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    spell_uuid = Column(String(36))
    date = Column(String(100), nullable=False)
    user_rel = relationship("User", back_populates="spells_rel_view")

class TypesOfSpells(Base):
    __tablename__ = 'type_of_spells'
    id = Column(Integer(), primary_key=True)
    name_of_type = Column(String(100))
    file = Column(String(100))


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    session = Session(bind=engine)
    type = TypesOfSpells(name_of_type="Charm", file="charms_il.jpg")
    session.add(type)
    type = TypesOfSpells(name_of_type="Transfiguration", file='transfiguration_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="DarkCharm", file='DarkCharm_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="Curse", file='curse_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="BindingMagicalContract", file='BindingMagicalContract_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="Vanishment", file='Vanishment_il.jpg')
    session.add(type)
    session.commit()
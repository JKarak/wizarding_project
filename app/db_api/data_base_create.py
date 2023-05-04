from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


Base = declarative_base()

class User(Base):  # 1
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    password_login_hash = Column(String(128), nullable=False)
    email = Column(String(100), nullable=False)
    avatar_file = Column(String(200), default='assets/avatar_0.jpg')
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

class Spells(Base):
    __tablename__ = 'spells'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    name = Column(String(100))
    incantation = Column(String(100))
    effect = Column(String(100))
    canBeVerbal = Column(String(100))
    type = Column(String(100))
    light = Column(String(100))
    creator = Column(String(100))
    picture = Column(String(200), default='assets/spell_0.jpg')

class Potions(Base):
    __tablename__ = 'potions'
    id = Column(Integer(), primary_key=True, autoincrement=True)
    uuid = Column(String(36))
    name = Column(String(100))
    effect = Column(String(100))
    sideEffects = Column(String(100))
    characteristics = Column(String(100))
    time = Column(String(100))
    difficulty = Column(String(100))
    #ingredients = relationship('IngredientsForPotion', back_populates="pot_rel")
    ingredients = Column(String(200))
    inventors = Column(String(200))
    manufacturer = Column(String(100))
    picture = Column(String(200), default='assets/potion_0.jpg')


'''class Ingredients(Base):
    __tablename__ = 'ingridients'
    id = Column(Integer(), primary_key=True)
    uuid = Column(String(36), nullable=False)
    name = Column(String(100), nullable=False)
    potions = relationship('IngredientsForPotion', back_populates="ingr_rel")

class IngredientsForPotion(Base):
    __tablename__ = 'ingridients_for_potion'
    id = Column(Integer(), primary_key=True)
    potion_uuid = Column(String(36), ForeignKey('potion.id'))
    ingr_uuid = Column(String(100), ForeignKey('ingredients.id'))
    pot_rel = relationship("Potions", back_populates="potions")
    ingr_rel = relationship("Ingredients", back_populates="ingredients")'''


if __name__ == '__main__':
    engine = create_engine("sqlite:///harry_potter_data.db", connect_args={'check_same_thread': True})

    Base.metadata.create_all(engine)

    session = Session(bind=engine)
    type = TypesOfSpells(name_of_type="Charm", file="assets/charms_il.jpg")
    session.add(type)
    type = TypesOfSpells(name_of_type="Transfiguration", file='assets/transfiguration_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="DarkCharm", file='assets/DarkCharm_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="Curse", file='assets/curse_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="BindingMagicalContract", file='assets/BindingMagicalContract_il.jpg')
    session.add(type)
    type = TypesOfSpells(name_of_type="Vanishment", file='assets/Vanishment_il.jpg')
    session.add(type)
    session.commit()
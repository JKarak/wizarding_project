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
    avatar_file = Column(String(200), default='avatar_0.jpg')
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
    id = Column(Integer(), primary_key=True)
    uuid = Column(String(36), primary_key=True)
    name = Column(String(100), nullable=False)
    incantation = Column(String(100), nullable=False)
    effect = Column(String(100), nullable=False)
    canBeVerbal = Column(String(100), nullable=False)
    type = Column(String(100), nullable=False)
    light = Column(String(100), nullable=False)
    creator = Column(String(100), nullable=False)

class Potions(Base):
    __tablename__ = 'potionss'
    id = Column(Integer(), primary_key=True)
    uuid = Column(String(36), nullable=False)
    name = Column(String(100), nullable=False)
    effect = Column(String(100), nullable=False)
    sideEffects = Column(String(100), nullable=False)
    characteristics = Column(String(100), nullable=False)
    time = Column(String(100), nullable=False)
    difficulty = Column(String(100), nullable=False)
    #ingredients = relationship('IngredientsForPotion', back_populates="pot_rel")
    ingredients = Column(String(200), nullable=False)
    inventors = Column(String(200), nullable=False)
    manufacturer = Column(String(100), nullable=False)


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
from sqlalchemy import create_engine, MetaData, Table, Integer, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine("sqlite:///harry_potter_data.db")

Base = declarative_base()

class User(Base):  # 1
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    name = Column(String(100), nullable=False)
    login = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    avatar_file = Column(String(200), default='0')
    date_create = Column(String(100), nullable=False)
    potions_rel_fav = relationship("FavouritePotions", back_populates="user_rel")
    potions_rel_view = relationship("ViewedPotions", back_populates="user_rel")
    spells_rel_fav = relationship("FavouriteSpells", back_populates="user_rel")
    spells_rel_view = relationship("ViewedSpells", back_populates="user_rel")

class FavouritePotions:
    __tablename__ = 'favourite_potions'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    potion_uuid = Column(String(36))
    active = Column(Integer(), unique=False)
    date = Column(String(100), nullable=False)
    user_rel = relationship("User", back_populates="potions_rel_fav")


class ViewedPotions:
    __tablename__ = 'viewed_potions'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    potion_uuid = Column(String(36))
    date = Column(String(100), nullable=False)
    user_rel = relationship("User", back_populates="potions_rel_view")

class FavouriteSpells:
    __tablename__ = 'favourite_spells'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    spell_uuid = Column(String(36))
    active = Column(Integer(), unique=False)
    date = Column(String(100), nullable=Fale)
    user_rel = relationship("User", back_populates="potions_rel_fav")


class ViewedSpells:
    __tablename__ = 'viewed_spells'
    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('users.id'))
    spell_uuid = Column(String(36))
    date = Column(String(100), nullable=False)
    user_rel = relationship("User", back_populates="potions_rel_view")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
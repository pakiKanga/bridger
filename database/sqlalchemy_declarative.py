import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Room(Base):
    __tablename__ = 'room'
    # Here we define columns for the table Room
    # Notice that each column is also a normal Python instance attribute
    id = Column(Integer, primary_key=True)
    room_name = Column(String(250))
    number_of_users = Column(Integer, nullable=False)
    created_date = Column(Date, nullable=False)
    room_key = Column(String(250), nullable = False)

class Registered_User(Base):
    __tablename__ = 'registered_user'
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)
    number_of_sessions = Column(Integer, nullable=False)

class User(Base):
    __tablename__ = 'user'
    # Here we define columns for a table user
    # Notice that each olumn is also a normal Python instance attribute
    id = Column(Integer, primary_key=True)
    entry_point = Column(Date, nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'))
    user_id = Column(Integer, ForeignKey('registered_user.id'))
    room = relationship(Room)
    registered_user = relationship(Registered_User)
    active = Column(Boolean, nullable = False)
    tagname = Column(String(250), nullable = False)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file
engine = create_engine('sqlite:///meetup.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL
# Drop all tables
# Base.metadata.drop_all(engine)
# Create all tables
Base.metadata.create_all(engine)

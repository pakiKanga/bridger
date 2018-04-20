from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.sqlalchemy_declarative import Base, Room, User, Registered_User

import datetime
from time import gmtime, strftime
import string
import random

engine = create_engine('sqlite:///meetup.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance stablishes all conversations with thedatabase
# and represents a 'staging zone' for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Creates a user - Allows user to be specified into a room
def create_user(room_id, user_id, room, registered_user, tagname):
    active = False
    if(room_id is not None and room is not None):
        # Increment number of users in room
        room.number_of_users += 1
        active = True
    user =  User(entry_point = strftime("%Y-%m-%d %H:%M:%S", gmtime()), room_id = room_id,  user_id = user_id, room = room, registered_user = registered_user, active = active, tagname = tagname)
    session.add(user)
    session.commit()
    return user

# User creates a room - Only users can create a room
def create_room(user, name):
    # Only inactive users can create a room
    if(user.active == True):
        raise Exception('User is already in a room! Check your code!')
    # Create a random key
    random_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
    # Create a Room
    room = Room(room_name = name, number_of_users = 0, created_date = strftime("%Y-%m-%d %H:%M:%S", gmtime()), room_key = random_key)
    # Add user to room
    session.add(room)
    session.commit()
    join_room(user, room)
    return room, random_key

# User joins a room
def join_room(user, room):
    user.room_id = room.id
    user.room = room
    user.active = True
    # Increment number of users in room
    room.number_of_users += 1
    session.commit()

# User leaves room
def leave_room(user):
    user.active = False
    user.room.number_of_users -= 1
    session.commit()

def find_room(room_key):
    room = session.query(Room).filter(Room.room_key == room_key).first()
    return room
# Insert a Person in the person table
# room = Room(id = 1, room_name = "BLAZE", number_of_users = 0, created_date = strftime("%Y-%m-%d %H:%M:%S", gmtime()), room_key = "ABC")
# session.commit()

# user1 = create_user(1, 1, None, None, None)
# user2 = create_user(2, 1, None, None, None)

# _ , random_key = create_room(user1, 'hallelujah')
# room = find_room(random_key)
# join_room(user2, room)
# print('number of users', room.number_of_users)
# print('user1:',user1.active,'user2:',user2.active)
# leave_room(user1)
# leave_room(user2)
# print('number of users', room.number_of_users)
# print('user1:',user1.active,'user2:',user2.active)

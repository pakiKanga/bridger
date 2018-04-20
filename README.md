# MeetupPoint
An application that gets the locations of a group of users, and finds optimal meetup points.

## Requirements
Install all the dependencies

```
pip install -r requirements.txt
```

## Database
This step requires that a database to be running locally or on a remote server.
Create your own setup.py file as such:

```
import os

SECRET_KEY = *YOUR_SECRET_KEY*
DEBUG=True
SQLALCHEMY_TRACK_MODIFICATIONS = True

# database configuration settings
DB_USERNAME = 'USER_NAME'
DB_PASSWORD = 'PASSWORD'
DATABASE_NAME = 'DBNAME'
DB_HOST = os.getenv('IP','HOSTNAME')
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI

```

Run the following commands to intialise and migrate the database.

```
python manage.py db init
python manage.py db migrate

# if updating from previous revision
python manage.py db upgrade
```

## Running

Run the server and enjoy.

```
python manage.py runserver
```

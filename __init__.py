from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bridger import setup

# creating an instance of the Flask app
app = Flask(__name__)

# setting the configuration of the application from a settings file
app.config.from_object('setup')
app.config['GOOGLE_API_KEY'] = 'AIzaSyAavEzAtMJulJUW-zw27g4pqZ3u21fLQKg'
app.config.from_object('configmodule.DevelopmentConfig')

# db holds the database
db = SQLAlchemy(app)

# migrations 
migrate = Migrate(app, db)

# importing all of the views from the various modules
from BridgerViews import views

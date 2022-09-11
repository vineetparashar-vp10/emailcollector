from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
from os import path


app = Flask(__name__);
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///main.db"
app.config['SQLALCHEME_TRACK_MODIFICATIONS'] = True
app.config['DEBUG'] = True

db = SQLAlchemy(app);
app.secret_key = "Roses_are_red"

from App import routes
from App.models import UserModel

def create_database():
	if not path.exists('App/mail.db'):
		db.create_all();

create_database();
'''
Created on 03/02/2014

@author: Herminio
'''
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/landportal'
db = SQLAlchemy(app)

from src.app import views

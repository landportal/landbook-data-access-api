"""
Created on 03/02/2014

:author: Weso
"""
from flask.app import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/landportal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from app import views

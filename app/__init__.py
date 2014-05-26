"""
Created on 03/02/2014
This file make the setup configuration for the Flask-Server

:author: Weso
"""
from flask.app import Flask
from flask.ext.cache import Cache
from flask.ext.track_usage import TrackUsage
from flask.ext.track_usage.storage.sql import SQLStorage
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/landportal'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'exclude'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
app.config['DEBUG'] = True
db = SQLAlchemy(app)
#sql_database_storage = SQLStorage('mysql+mysqlconnector://root:root@localhost:3306/landportal', table_name='api_usage')
sql_database_storage = SQLStorage('sqlite:///analytics.db', table_name='api_usage')
t = TrackUsage(app, sql_database_storage)

from app import views

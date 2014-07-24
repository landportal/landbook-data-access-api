# -*- coding: utf-8 -*-

# landportal-data-access-api
# Copyright (c)2014, WESO, Web Semantics Oviedo.
# Written by Herminio García.

# This file is part of landportal-data-access-api.
#
# landportal-data-access-api is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License.
#
# landportal-data-access-api is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with landportal-data-access-api.  If not, see <http://www.gnu.org/licenses/>.

# landportal-data-access-api is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>

"""
Created on 03/02/2014
This file make the setup configuration for the Flask-Server

:author: Herminio García
"""
from flask.app import Flask
from flask.ext.cache import Cache
from flask.ext.track_usage import TrackUsage
from flask.ext.track_usage.storage.sql import SQLStorage
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost:3306/landportal'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
app.config['TRACK_USAGE_USE_FREEGEOIP'] = False
app.config['TRACK_USAGE_INCLUDE_OR_EXCLUDE_VIEWS'] = 'exclude'
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
#cache = Cache(app, config={'CACHE_TYPE': 'memcached', 'CACHE_MEMCACHED_SERVERS': ['5.9.221.11:11211']})
app.config['DEBUG'] = True
db = SQLAlchemy(app)
#sql_database_storage = SQLStorage('mysql+mysqlconnector://root:root@localhost:3306/landportal', table_name='api_usage')
sql_database_storage = SQLStorage('sqlite:///analytics.db', table_name='api_usage')
t = TrackUsage(app, sql_database_storage)

from app import views

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
Created on 10/02/2014

:author: Herminio García
"""
from app import db


if __name__ == '__main__':
    db.create_all()
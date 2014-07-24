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
This file includes some util features like marshalling

:author: Herminio García
"""

import json
import datetime, time
from dicttoxml import dicttoxml


class JSONConverter(object):
    """
    JSON converter from objects and list
    """
    def list_to_json(self, elements_list):
        """
        Convert a list to its json equivalent

        :param elements_list: list of elements to be converted
        :return: json array ready be returned as string
        """
        json_result = '[\n'
        for element in elements_list:
            json_result += self.object_to_json(element) + ",\n" \
                if len(elements_list)-1 != elements_list.index(element) \
                else self.object_to_json(element) + "\n"
        json_result += "]"
        return json_result
        
    def object_to_json(self, element):
        """
        Convert a object to its json equivalent

        :param element: element to be converted
        :return: json object in string format
        """
        return json.dumps(row2dict(element))


class XMLConverter(object):
    """
    XML converter from objects and list
    """
    
    def __init__(self):
        """
        Constructor for XML converter
        """
        self.json_converter = JSONConverter()  # needed, first to json and then to xml
    
    def list_to_xml(self, elements_list, root_node="elements", child_node="element"):
        """
        Convert a list to its XML equivalent

        :param elements_list: list of elements to be converted
        :param root_node: name for the root tag in the xml, by default *elements*
        :param child_node: name for object tag in every element of the list, by default *element*
        :return: Xml string
        """
        xml_result = '<' + root_node + '>'
        for element in elements_list:
            xml_result += self.object_to_xml(element, child_node)
        xml_result += '</' + root_node + '>'
        return xml_result

    def object_to_xml(self, element, root_node="element"):
        """
        Convert a object to its XML equivalent

        :param element: element to be converted
        :param root_node: name for root tag on xml, by default *element*
        :return: Xml string
        """
        element = json.loads(self.json_converter.object_to_json(element))
        xml_result = '<' + root_node + '>'
        xml_result += dicttoxml(element, False)        
        xml_result += '</' + root_node + '>'
        return xml_result


class CSVConverter(object):
    """
    CSV converter from objects and list
    """

    def list_to_csv(self, elements_list):
        """
        Convert a list to its csv equivalent

        :param elements_list: collection to be converted
        :return: csv string
        """
        csv_result = ''
        keys = row2dict(elements_list[0]).keys()
        csv_result += ';'.join(keys) + '\n'
        for element in elements_list:
            csv_result += self.object_to_csv(element, False, keys)
        return csv_result

    def object_to_csv(self, element, header=True, keys=None):
        """
        Convert a object to its csv equivalent

        :param element: object to be converted
        :param header: True if headers are desired, False if not, by default True
        :param keys: Header keys to use if method used by list_to_csv, default None
        :return: csv string
        """
        element = row2dict(element)
        csv = ''
        if keys is None:
            keys = element.keys()
        if header:
            csv += ';'.join(element.keys()) + '\n'
        for key in keys:
            if key in element.keys():
                try:
                    value = str(element[key])
                except UnicodeEncodeError:
                    value = element[key]
            else:
                value = ''
            csv += value + ';'
        csv += '\n'
        return csv


class Struct(object):
    """
    Class to convert from dictionary to object

    :see: http://stackoverflow.com/questions/1305532/convert-python-dict-to-object/1305663#1305663
    """
    def __init__(self, **entries): 
        self.__dict__.update(entries)


class DictionaryList2ObjectList(object):
    """
    Class to convert from a list of dictionaries to a list of objects
    """
    def convert(self, given_list):
        """
        Convert a list of dictionaries in a list of objects

        :param given_list: list of dictionaries
        :return: list of object
        """
        returned_list = []
        for element in given_list:
            returned_list.append(Struct(**element))
        return returned_list


def check_if_date(field_name, object, row):
    """
    Convert a date field into long format

    :param field_name: name of the field where the date is
    :param object: object to store the date in long format
    :param row: object, usually a SQLAlchemy row where field is stored
    """
    if type(getattr(row, field_name)) is datetime.date or type(getattr(row, field_name)) is datetime.datetime:
        object[field_name] = time.mktime(getattr(row, field_name).timetuple())
    else:
        object[field_name] = getattr(row, field_name)


def row2dict(row):
    """
    Converts a row of SQLAlchemy into a dictionary

    :see: http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    :param row: SQLAlchemy row
    :return: dictionary
    """
    if row is None:
        return None
    d = {}
    if hasattr(row, '__table__'):
        for column in row.__mapper__.columns:
            check_if_date(column.name, d, row)
        if hasattr(row, 'other_parseable_fields'):
            for field in row.other_parseable_fields:
                result = is_primitive(getattr(row, field))
                if isinstance(getattr(row, field), object) and not is_primitive(getattr(row, field)):
                    d[field] = row2dict(getattr(row, field))
                else:
                    check_if_date(field, d, row)
        return d
    else:
        for column in get_user_attrs(row):
            check_if_date(column, d, row)
        return d


def get_user_attrs(object):
    """
    Return the attributes of an object

    :param object: the object to get attributes from
    :return: list of attributes
    """
    return [k for k in dir(object)
            if not k.startswith('__')
            and not k.endswith('__')]


def is_primitive(thing):
    """
    Check whether a object is of a primitive type or not

    :param thing: object to check if its type is primitive
    :return: True if it is primitive, else False
    """
    primitive = (int, str, bool, float, unicode)
    return type(thing) in primitive
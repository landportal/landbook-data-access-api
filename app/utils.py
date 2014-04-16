'''
Created on 03/02/2014

@author: Herminio
'''
import json
import datetime, time
from dicttoxml import dicttoxml


class JSONConverter(object):
    '''
    JSON converter from objects and list
    '''
    
    def list_to_json(self, elements_list):
        '''
        Convert a list to its json equivalent
        '''
        json_result = '[\n'
        for element in elements_list:
            json_result += self.object_to_json(element) + ",\n" \
                if len(elements_list)-1 != elements_list.index(element) \
                else self.object_to_json(element) + "\n"
        json_result += "]"
        return json_result
        
    def object_to_json(self, element):
        '''
        Convert a object to its json equivalent
        '''
        return json.dumps(row2dict(element))


class XMLConverter(object):
    '''
    XML converter from objects and list
    '''
    
    def __init__(self):
        '''
        Constructor for XML converter
        '''
        self.json_converter = JSONConverter()
    
    def list_to_xml(self, elements_list, root_node="elements", child_node="element"):
        '''
        Convert a list to its XML equivalent
        '''
        xml_result = '<' + root_node + '>'
        for element in elements_list:
            xml_result += self.object_to_xml(element, child_node)
        xml_result += '</' + root_node + '>'
        return xml_result

    def object_to_xml(self, element, root_node="element"):
        '''
        Convert a object to its XML equivalent
        '''
        element = json.loads(self.json_converter.object_to_json(element))
        xml_result = '<' + root_node + '>'
        xml_result += dicttoxml(element, False)        
        xml_result += '</' + root_node + '>'
        return xml_result


class CSVConverter(object):
    '''
    CSV converter from objects and list
    '''

    def list_to_csv(self, elements_list):
        '''
        Convert a list to its json equivalent
        '''
        csv_result = ''
        keys = row2dict(elements_list[0]).keys()
        csv_result += ';'.join(keys) + '\n'
        for element in elements_list:
            csv_result += self.object_to_csv(element, False, keys)
        return csv_result

    def object_to_csv(self, element, header=True, keys=None):
        '''
        Convert a object to its json equivalent
        '''
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
    '''
    Class to convert from dictionary to object
    @see: http://stackoverflow.com/questions/1305532/convert-python-dict-to-object/1305663#1305663
    '''
    def __init__(self, **entries): 
        self.__dict__.update(entries)
        
class DictionaryList2ObjectList(object):
    '''
    Class to convert from a list of dictionaries to a list of objects
    '''
    def convert(self, given_list):
        returned_list = []
        for element in given_list:
            returned_list.append(Struct(**element))
        return returned_list


def check_if_date(field_name, object, row):
    if type(getattr(row, field_name)) is datetime.date or type(getattr(row, field_name)) is datetime.datetime:
        object[field_name] = time.mktime(getattr(row, field_name).timetuple())
    else:
        object[field_name] = getattr(row, field_name)


def row2dict(row):
    '''
    @see: http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    '''
    if row is None:
        return None
    d = {}
    if hasattr(row, '__table__'):
        for column in row.__table__.columns:
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
    return [k for k in dir(object)
            if not k.startswith('__')
            and not k.endswith('__')]


def is_primitive(thing):
    primitive = (int, str, bool, float, unicode)
    return type(thing) in primitive
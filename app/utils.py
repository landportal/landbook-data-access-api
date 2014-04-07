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

def row2dict(row):
    '''
    @see: http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    '''
    if row is None:
        return None
    d = {}
    if hasattr(row, '__table__'):
        for column in row.__table__.columns:
            if type(getattr(row, column.name)) is datetime.datetime:
                d[column.name] = time.mktime(getattr(row, column.name).timetuple())
            else:
                d[column.name] = getattr(row, column.name)
        return d
    else:
        for column in get_user_attrs(row):
            if type(getattr(row, column)) is datetime.datetime:
                d[column] = time.mktime(getattr(row, column).timetuple())
            else:
                d[column] = getattr(row, column)
        return d


def get_user_attrs(object):
    return [k for k in dir(object)
            if not k.startswith('__')
            and not k.endswith('__')]
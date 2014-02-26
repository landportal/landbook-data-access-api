'''
Created on 03/02/2014

@author: Herminio
'''
import json
from dicttoxml import dicttoxml
from models import Country

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
        return json.dumps(row2dict(element, Country))
    
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

def row2dict(row, cls):
    '''
    @see: http://stackoverflow.com/questions/1958219/convert-sqlalchemy-row-object-to-python-dict
    '''
    object = cls()
    d = {}
    for column in dir(row):
        if hasattr(object, column) and column[0] is not "_":
            d[column] = getattr(row, column)
    return d
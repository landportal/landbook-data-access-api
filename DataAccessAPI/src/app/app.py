'''
Created on 03/02/2014

@author: Herminio
'''
from flask.app import Flask
from src.service.services import CountryService
from src.model.models import Country
from src.util.utils import JSONConverter, XMLConverter,\
    DictionaryList2ObjectList
from flask.wrappers import Response
from flask.globals import request
from werkzeug.exceptions import abort
from flask.helpers import url_for
from flask_restful import Api, Resource
from flask import json

country_service = CountryService()
json_converter = JSONConverter()
xml_converter = XMLConverter()
list_converter = DictionaryList2ObjectList()
app = Flask(__name__)
api = Api(app)

class CountryListAPI(Resource):
    '''
    Countries collection URI
    Methods: GET, POST, PUT, DELETE  
    '''
    
    def get(self):
        '''
        List all countries
        Response 200 OK
        '''
        if is_json_accepted(request):
            return Response(json_converter.list_to_json(country_service.get_all_countries()
                                                        ), mimetype='application/json')
        else:
            return Response(xml_converter.list_to_xml(country_service.get_all_countries(), 
                                                      'countries', 'country'), mimetype='application/xml')
    
    def post(self):
        '''
        Create a new country
        Response 201 CREATED
        @return: URI
        '''
        country = Country(request.json.get("name"), request.json.get("fao_URI"), 
                          request.json.get("iso_code2"), request.json.get("iso_code3"))
        if country.iso_code2 is not None and country.iso_code3 is not None:
            country_service.insert_country(country)
            return {'URI': url_for('countries', code=country.iso_code3)} #returns the URI for the new country
        abort(400) # in case something is wrong
    
    def put(self):
        '''
        Update all countries given
        Response 204 NO CONTENT
        '''
        country_list = json.loads(request.data)
        country_list = list_converter.convert(country_list)
        country_service.update_countries(country_list)
        return {}, 204 
    
    def delete(self):
        '''
        Delete all countries
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        country_service.delete_all_countries()
        return {}, 204
        
class CountryAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''
    
    def get(self, code):
        '''
        Show country
        Response 200 OK
        '''
        if is_json_accepted(request):
            return Response(json_converter.object_to_json(country_service.get_country_by_code(code)
                                                          ), mimetype='application/json')
        else:
            return Response(xml_converter.object_to_xml(country_service.get_country_by_code(code), 
                                                        'country'), mimetype='application/xml')
    
    def put(self, code):
        '''
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        country = country_service.get_country_by_code(code)
        if country is not None:
            country.iso_code2 = request.json.get("iso_code2")
            country.fao_URI = request.json.get("fao_URI")
            country.name = request.json.get("name")
            country_service.update_country(country)
            return {}, 204
        else:
            abort(400)
    
    def delete(self, code):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        country_service.delete_country(code)
        return {}, 204
    
api.add_resource(CountryListAPI, '/api/countries', endpoint = 'countries_list')
api.add_resource(CountryAPI, '/api/countries/<code>', endpoint = 'countries')
      
def is_json_accepted(request):
    '''
    Returns if json is accepted or not, returns json as default
    '''
    return "application/json" in request.accept_mimetypes or "text/json" in request.accept_mimetypes

if __name__ == '__main__':
    app.run(debug=True)

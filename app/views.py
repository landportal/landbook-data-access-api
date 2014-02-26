'''
Created on 03/02/2014

@author: Herminio
'''
from flask_restful import Resource, abort, Api
from flask.wrappers import Response
from flask.helpers import url_for
from flask import json
from app import app
from app.utils import JSONConverter, XMLConverter, DictionaryList2ObjectList
from app.models import Country
from app.services import CountryService, IndicatorService
from flask import request

api = Api(app)
country_service = CountryService()
indicator_service = IndicatorService()
json_converter = JSONConverter()
xml_converter = XMLConverter()
list_converter = DictionaryList2ObjectList()


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
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(country_service.get_all(),
                                                      'countries', 'country'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(country_service.get_all()
                                                        ), mimetype='application/json')
    
    def post(self):
        '''
        Create a new country
        Response 201 CREATED
        @return: URI
        '''
        country = Country(request.json.get("name"), request.json.get("iso2"),
                          request.json.get("iso3"), request.json.get("fao_URI"))
        if country.iso2 is not None and country.iso3 is not None:
            country_service.insert(country)
            return {'URI': url_for('countries', code=country.iso3)} #returns the URI for the new country
        abort(400) # in case something is wrong
    
    def put(self):
        '''
        Update all countries given
        Response 204 NO CONTENT
        '''
        country_list = json.loads(request.data)
        country_list = list_converter.convert(country_list)
        country_service.update_all(country_list)
        return {}, 204 
    
    def delete(self):
        '''
        Delete all countries
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        country_service.delete_all()
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
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(country_service.get_by_code(code),
                                                        'country'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(country_service.get_by_code(code)
                                                          ), mimetype='application/json')
    
    def put(self, code):
        '''
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        country = country_service.get_by_code(code)
        if country is not None:
            country.iso_code2 = request.json.get("iso_code2")
            country.fao_URI = request.json.get("fao_URI")
            country.idRegion = request.json.get("idRegion")
            country_service.update(country)
            return {}, 204
        else:
            abort(400)
    
    def delete(self, code):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        country_service.delete(code)
        return {}, 204

class IndicatorListAPI(Resource):
    '''
    Indicators collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self):
        '''
        List all countries
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(indicator_service.get_all(),
                                                      'indicators', 'indicator'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(indicator_service.get_all()
                                                        ), mimetype='application/json')

    def post(self):
        '''
        Create a new country
        Response 201 CREATED
        @return: URI
        '''
        country = Country(request.json.get("name"), request.json.get("iso2"),
                          request.json.get("iso3"), request.json.get("fao_URI"))
        if country.iso2 is not None and country.iso3 is not None:
            country_service.insert(country)
            return {'URI': url_for('countries', code=country.iso3)} #returns the URI for the new country
        abort(400) # in case something is wrong

    def put(self):
        '''
        Update all countries given
        Response 204 NO CONTENT
        '''
        country_list = json.loads(request.data)
        country_list = list_converter.convert(country_list)
        country_service.update_all(country_list)
        return {}, 204

    def delete(self):
        '''
        Delete all countries
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        country_service.delete_all()
        return {}, 204

class IndicatorAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, code):
        '''
        Show country
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(country_service.get_by_code(code),
                                                        'country'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(country_service.get_by_code(code)
                                                          ), mimetype='application/json')

    def put(self, code):
        '''
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        country = country_service.get_by_code(code)
        if country is not None:
            country.iso_code2 = request.json.get("iso_code2")
            country.fao_URI = request.json.get("fao_URI")
            country.idRegion = request.json.get("idRegion")
            country_service.update(country)
            return {}, 204
        else:
            abort(400)

    def delete(self, code):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        country_service.delete(code)
        return {}, 204
    
api.add_resource(CountryListAPI, '/api/countries', endpoint = 'countries_list')
api.add_resource(CountryAPI, '/api/countries/<code>', endpoint = 'countries')
api.add_resource(IndicatorListAPI, '/api/indicators', endpoint = 'indicators_list')
api.add_resource(IndicatorAPI, '/api/indicators/<id>', endpoint = 'indicators')
      
def is_xml_accepted(request):
    '''
    Returns if json is accepted or not, returns json as default
    '''
    return request.args.get('format') == "xml"
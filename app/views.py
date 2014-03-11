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
from model.models import Country, Indicator, User, Organization
from app.services import CountryService, IndicatorService, UserService, OrganizationService
from flask import request

api = Api(app)
country_service = CountryService()
indicator_service = IndicatorService()
user_service = UserService()
organization_service = OrganizationService()
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
            return {'URI': url_for('countries', code=country.iso3)}, 201 #returns the URI for the new country
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
        country = country_service.get_by_code(code)
        if country is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(country,
                                                        'country'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(country
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
            country.iso2 = request.json.get("iso2")
            country.fao_URI = request.json.get("fao_URI")
            country.name = request.json.get("name")
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
        Create a new indicator
        Response 201 CREATED
        @return: URI
        '''
        indicator = Indicator(request.json.get("id"), request.json.get("name"),
                              request.json.get("description"), request.json.get("measurement_unit_id"),
                              request.json.get("dataset_id"), request.json.get("compound_indicator_id"))
        if indicator.name is not None:
            indicator_service.insert(indicator)
            return {'URI': url_for('indicators', id=indicator.id)}, 201 #returns the URI for the new indicator
        abort(400) # in case something is wrong

    def put(self):
        '''
        Update all countries given
        Response 204 NO CONTENT
        '''
        indicator_list = json.loads(request.data)
        indicator_list = list_converter.convert(indicator_list)
        indicator_service.update_all(indicator_list)
        return {}, 204

    def delete(self):
        '''
        Delete all countries
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        indicator_service.delete_all()
        return {}, 204

class IndicatorAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id):
        '''
        Show country
        Response 200 OK
        '''
        indicator = indicator_service.get_by_code(id)
        if indicator is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(indicator,
                                                        'indicator'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(indicator
            ), mimetype='application/json')

    def put(self, id):
        '''
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        indicator = indicator_service.get_by_code(id)
        if indicator is not None:
            indicator.name = request.json.get("name")
            indicator.description = request.json.get("description")
            indicator.measurement_unit_id = request.json.get("measurement_unit_id")
            indicator.dataset_id = request.json.get("dataset_id")
            indicator.compound_indicator_id = request.json.get("compound_indicator_id")
            indicator_service.update(indicator)
            return {}, 204
        else:
            abort(400)

    def delete(self, id):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        indicator_service.delete(id)
        return {}, 204

class UserListAPI(Resource):
    '''
    Users collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self):
        '''
        List all users
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(user_service.get_all(),
                                                      'users', 'user'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(user_service.get_all()
                                                        ), mimetype='application/json')

    def post(self):
        '''
        Create a new user
        Response 201 CREATED
        @return: URI
        '''
        user = User(request.json.get("id"), request.json.get("ip"),
                    request.json.get("timestamp"), request.json.get("organization_id"))
        if user.id is not None:
            country_service.insert(user)
            return {'URI': url_for('users', id=user.id)}, 201  # returns the URI for the new user
        abort(400)  # in case something is wrong

    def put(self):
        '''
        Update all countries given
        Response 204 NO CONTENT
        '''
        user_list = json.loads(request.data)
        user_list = list_converter.convert(user_list)
        user_service.update_all(user_list)
        return {}, 204

    def delete(self):
        '''
        Delete all countries
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        user_service.delete_all()
        return {}, 204

class UserAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id):
        '''
        Show country
        Response 200 OK
        '''
        user = user_service.get_by_code(id)
        if user is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(user,
                                                        'user'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(user
                                                          ), mimetype='application/json')

    def put(self, id):
        '''
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        user = user_service.get_by_code(id)
        if user is not None:
            user.id = request.json.get("id")
            user.ip = request.json.get("ip")
            user.timestamp = request.json.get("timestamp")
            user.organization_id = request.json.get("organization_id")
            user_service.update(user)
            return {}, 204
        else:
            abort(400)

    def delete(self, id):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        user_service.delete(id)
        return {}, 204

class OrganizationListAPI(Resource):
    '''
    Organizations collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self):
        '''
        List all organizations
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(organization_service.get_all(),
                                                      'organizations', 'organization'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(organization_service.get_all()
                                                        ), mimetype='application/json')

    def post(self):
        '''
        Create a new organization
        Response 201 CREATED
        @return: URI
        '''
        organization = Organization(request.json.get("id"), request.json.get("name"),
                                    request.json.get("url"), request.json.get("is_part_of_id"))
        if organization.id is not None:
            organization_service.insert(organization)
            return {'URI': url_for('organizations', id=organization.id)}, 201  # returns the URI for the new user
        abort(400)  # in case something is wrong

    def put(self):
        '''
        Update all countries given
        Response 204 NO CONTENT
        '''
        organization_list = json.loads(request.data)
        organization_list = list_converter.convert(organization_list)
        organization_service.update_all(organization_list)
        return {}, 204

    def delete(self):
        '''
        Delete all countries
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        organization_service.delete_all()
        return {}, 204

class OrganizationAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id):
        '''
        Show country
        Response 200 OK
        '''
        organization = organization_service.get_by_code(id)
        if organization is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(organization,
                                                        'organization'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(organization
                                                          ), mimetype='application/json')

    def put(self, id):
        '''
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        organization = organization_service.get_by_code(id)
        if organization is not None:
            organization.id = request.json.get("id")
            organization.name = request.json.get("name")
            organization.url = request.json.get("url")
            organization.is_part_of_id = request.json.get("is_part_of_id")
            organization_service.update(organization)
            return {}, 204
        else:
            abort(400)

    def delete(self, id):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        organization_service.delete(id)
        return {}, 204

class OrganizationUserListAPI(Resource):
    '''
    Organizations users collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self, organization_id):
        '''
        List all organizations
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(organization_service.get_by_code(organization_id).users,
                                                      'users', 'user'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(organization_service.get_by_code(organization_id).users
                                                        ), mimetype='application/json')


class OrganizationUserAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, organization_id, user_id):
        '''
        Show country
        Response 200 OK
        '''
        selected_user = None
        for user in organization_service.get_by_code(organization_id).users:
            if user.id == int(user_id):
                selected_user = user
        if selected_user is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(selected_user,
                                                        'user'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(selected_user
                                                          ), mimetype='application/json')


api.add_resource(CountryListAPI, '/api/countries', endpoint='countries_list')
api.add_resource(CountryAPI, '/api/countries/<code>', endpoint='countries')
api.add_resource(IndicatorListAPI, '/api/indicators', endpoint='indicators_list')
api.add_resource(IndicatorAPI, '/api/indicators/<id>', endpoint='indicators')
api.add_resource(UserListAPI, '/api/users', endpoint='users_list')
api.add_resource(UserAPI, '/api/users/<id>', endpoint='users')
api.add_resource(OrganizationListAPI, '/api/organizations', endpoint='organizations_list')
api.add_resource(OrganizationAPI, '/api/organizations/<id>', endpoint='organizations')
api.add_resource(OrganizationUserListAPI, '/api/organizations/<organization_id>/users', endpoint='organizations_users_list')
api.add_resource(OrganizationUserAPI, '/api/organizations/<organization_id>/users/<user_id>', endpoint='organizations_users')

def is_xml_accepted(request):
    '''
    Returns if json is accepted or not, returns json as default
    '''
    return request.args.get('format') == "xml"
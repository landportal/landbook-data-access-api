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
from model.models import Country, Indicator, User, Organization, Observation, Region, DataSource, Dataset
from app.services import CountryService, IndicatorService, UserService, OrganizationService, ObservationService, \
    RegionService, DataSourceService, DatasetService
from flask import request

api = Api(app)
country_service = CountryService()
indicator_service = IndicatorService()
user_service = UserService()
organization_service = OrganizationService()
observation_service = ObservationService()
region_service = RegionService()
datasource_service = DataSourceService()
dataset_service = DatasetService()
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
        country.is_part_of_id = request.json.get("is_part_of_id")
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


class CountriesIndicatorListAPI(Resource):
    '''
    Countries Indicator collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self, iso3):
        '''
        List all organizations
        Response 200 OK
        '''
        observations = country_service.get_by_code(iso3).observations
        indicators = []
        for obs in observations:
            if obs.indicator is not None:
                indicators.append(obs.indicator)
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(indicators,
                                                      'indicators', 'indicator'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(indicators
                                                        ), mimetype='application/json')


class CountriesIndicatorAPI(Resource):
    '''
    Countries Indicator element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, iso3, indicator_id):
        '''
        Show country
        Response 200 OK
        '''
        observations = country_service.get_by_code(iso3).observations
        indicator = None
        for obs in observations:
            if obs.indicator is not None and obs.indicator.id == int(indicator_id):
                indicator = obs.indicator
        if indicator is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(indicator,
                                                        'indicator'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(indicator
                                                          ), mimetype='application/json')

class ObservationListAPI(Resource):
    '''
    Observations collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self):
        '''
        List all observations
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(observation_service.get_all(),
                                                      'observations', 'observation'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(observation_service.get_all()
                                                        ), mimetype='application/json')

    def post(self):
        '''
        Create a new observation
        Response 201 CREATED
        @return: URI
        '''
        observation = Observation(request.json.get("id"), request.json.get("id_source"))
        observation.ref_time_id = request.json.get("ref_time_id")
        observation.issued_id = request.json.get("issued_id")
        observation.computation_id = request.json.get("computation_id")
        observation.indicator_group_id = request.json.get("indicator_group_id")
        observation.value_id = request.json.get("value_id")
        observation.indicator_id = request.json.get("indicator_id")
        observation.dataset_id = request.json.get("dataset_id")
        observation.region_id = request.json.get("region_id")
        observation.slice_id = request.json.get("slice_id")
        if observation.id is not None:
            organization_service.insert(observation)
            return {'URI': url_for('observations', id=observation.id)}, 201  # returns the URI for the new user
        abort(400) # in case something is wrong

    def put(self):
        '''
        Update all countries given
        Response 204 NO CONTENT
        '''
        observation_list = json.loads(request.data)
        observation_list = list_converter.convert(observation_list)
        observation_service.update_all(observation_list)
        return {}, 204

    def delete(self):
        '''
        Delete all countries
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        observation_service.delete_all()
        return {}, 204

class ObservationAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id):
        '''
        Show country
        Response 200 OK
        '''
        observation = observation_service.get_by_code(id)
        if observation is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(observation,
                                                        'observation'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(observation
                                                          ), mimetype='application/json')

    def put(self, id):
        '''
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        observation = observation_service.get_by_code(id)
        if observation is not None:
            observation.id_source = request.json.get("id_source")
            observation.ref_time_id = request.json.get("ref_time_id")
            observation.issued_id = request.json.get("issued_id")
            observation.computation_id = request.json.get("computation_id")
            observation.indicator_group_id = request.json.get("indicator_group_id")
            observation.value_id = request.json.get("value_id")
            observation.indicator_id = request.json.get("indicator_id")
            observation.dataset_id = request.json.get("dataset_id")
            observation.region_id = request.json.get("region_id")
            observation.slice_id = request.json.get("slice_id")
            return {}, 204
        else:
            abort(400)

    def delete(self, id):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        observation_service.delete(id)
        return {}, 204

class RegionListAPI(Resource):
    '''
    Regions collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self):
        '''
        List all region
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(region_service.get_all(),
                                                      'regions', 'region'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(region_service.get_all()
                                                        ), mimetype='application/json')

    def post(self):
        '''
        Create a new region
        Response 201 CREATED
        @return: URI
        '''
        region = Region(request.json.get("name"))
        region.id = request.json.get("id")
        region.is_part_of_id = request.json.get("is_part_of_id")
        if region.name is not None:
            region_service.insert(region)
            return {'URI': url_for('regions', id=region.id)}, 201 #returns the URI for the new region
        abort(400)  # in case something is wrong

    def put(self):
        '''
        Update all regions given
        Response 204 NO CONTENT
        '''
        region_list = json.loads(request.data)
        region_list = list_converter.convert(region_list)
        region_service.update_all(region_list)
        return {}, 204

    def delete(self):
        '''
        Delete all regions
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        region_service.delete_all()
        return {}, 204

class RegionAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id):
        '''
        Show region
        Response 200 OK
        '''
        region = region_service.get_by_code(id)
        if region is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(region,
                                                        'region'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(region
                                                          ), mimetype='application/json')

    def put(self, id):
        '''
        If exists update region
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        region = region_service.get_by_code(id)
        if region is not None:
            region.name = request.json.get("name")
            region.is_part_of_id = request.json.get("is_part_of_id")
            region_service.update(region)
            return {}, 204
        else:
            abort(400)

    def delete(self, id):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        region_service.delete(id)
        return {}, 204


class RegionsCountryListAPI(Resource):
    '''
    Regions Country collection URI
    Methods: GET
    '''

    def get(self, id):
        '''
        List all countries
        Response 200 OK
        '''
        countries = []
        for country in country_service.get_all():
            if country.is_part_of_id is int(id):
                countries.append(country)
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(countries,
                                                      'countries', 'country'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(countries
                                                        ), mimetype='application/json')


class RegionsCountryAPI(Resource):
    '''
    Countries Indicator element URI
    Methods: GET
    '''

    def get(self, id, iso3):
        '''
        Show country
        Response 200 OK
        '''
        selected_country = None
        for country in country_service.get_all():
            if country.is_part_of_id == int(id) and country.iso3 == iso3:
                selected_country = country
        if selected_country is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(selected_country,
                                                        'country'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(selected_country
                                                          ), mimetype='application/json')


class DataSourceListAPI(Resource):
    '''
    DataSource collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self):
        '''
        List all datasources
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(datasource_service.get_all(),
                                                      'datasources', 'datasource'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(datasource_service.get_all()
                                                        ), mimetype='application/json')

    def post(self):
        '''
        Create a new datasource
        Response 201 CREATED
        @return: URI
        '''
        datasource = DataSource(request.json.get("id_source"), request.json.get("name"))
        datasource.id = request.json.get("id")
        datasource.organization_id = request.json.get("organization_id")
        if datasource.name is not None:
            datasource_service.insert(datasource)
            return {'URI': url_for('datasources', id=datasource.id)}, 201 #returns the URI for the new datasource
        abort(400)  # in case something is wrong

    def put(self):
        '''
        Update all datasources given
        Response 204 NO CONTENT
        '''
        datasource_list = json.loads(request.data)
        datasource_list = list_converter.convert(datasource_list)
        datasource_service.update_all(datasource_list)
        return {}, 204

    def delete(self):
        '''
        Delete all datasources
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        datasource_service.delete_all()
        return {}, 204


class DataSourceAPI(Resource):
    '''
    Countries element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id):
        '''
        Show datasource
        Response 200 OK
        '''
        datasource = datasource_service.get_by_code(id)
        if datasource is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(datasource,
                                                        'datasource'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(datasource
                                                          ), mimetype='application/json')

    def put(self, id):
        '''
        If exists update datasource
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        datasource = datasource_service.get_by_code(id)
        if datasource is not None:
            datasource.id_source = request.json.get("id_source")
            datasource.name = request.json.get("name")
            datasource.organization_id = request.json.get("organization_id")
            datasource_service.update(datasource)
            return {}, 204
        else:
            abort(400)

    def delete(self, id):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        datasource_service.delete(id)
        return {}, 204


class DatasetListAPI(Resource):
    '''
    Dataset collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self):
        '''
        List all datasets
        Response 200 OK
        '''
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(dataset_service.get_all(),
                                                      'datasets', 'dataset'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(dataset_service.get_all()
                                                        ), mimetype='application/json')

    def post(self):
        '''
        Create a new dataset
        Response 201 CREATED
        @return: URI
        '''
        dataset = Dataset(request.json.get("id"))
        dataset.id_source = request.json.get("id_source")
        dataset.sdmx_frequency = request.json.get("sdmx_frequency")
        dataset.datasource_id = request.json.get("datasource_id")
        dataset.license_id = request.json.get("license_id")
        if dataset.id is not None:
            dataset_service.insert(dataset)
            return {'URI': url_for('datasets', id=dataset.id)}, 201 #returns the URI for the new dataset
        abort(400)  # in case something is wrong

    def put(self):
        '''
        Update all datasets given
        Response 204 NO CONTENT
        '''
        dataset_list = json.loads(request.data)
        dataset_list = list_converter.convert(dataset_list)
        dataset_service.update_all(dataset_list)
        return {}, 204

    def delete(self):
        '''
        Delete all datasets
        Response 204 NO CONTENT
        @attention: Take care of what you do, all countries will be destroyed
        '''
        dataset_service.delete_all()
        return {}, 204


class DatasetAPI(Resource):
    '''
    Dataset element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id):
        '''
        Show dataset
        Response 200 OK
        '''
        datasets = dataset_service.get_by_code(id)
        if datasets is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(datasets,
                                                        'datasets'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(datasets
                                                          ), mimetype='application/json')

    def put(self, id):
        '''
        If exists update dataset
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        '''
        dataset = dataset_service.get_by_code(id)
        if dataset is not None:
            dataset.id_source = request.json.get("id_source")
            dataset.sdmx_frequency = request.json.get("sdmx_frequency")
            dataset.datasource_id = request.json.get("datasource_id")
            dataset.license_id = request.json.get("license_id")
            return {}, 204
        else:
            abort(400)

    def delete(self, id):
        '''
        Delete country
        Response 204 NO CONTENT
        '''
        dataset_service.delete(id)
        return {}, 204


class DataSourceIndicatorListAPI(Resource):
    '''
    DataSource Indicator collection URI
    Methods: GET, POST, PUT, DELETE
    '''

    def get(self, id):
        '''
        List all indicators
        Response 200 OK
        '''
        datasets = datasource_service.get_by_code(id).datasets
        indicators = []
        for dataset in datasets:
            indicators.extend(dataset.indicators)
        if is_xml_accepted(request):
            return Response(xml_converter.list_to_xml(indicators,
                                                      'indicators', 'indicator'), mimetype='application/xml')
        else:
            return Response(json_converter.list_to_json(indicators
                                                        ), mimetype='application/json')


class DataSourceIndicatorAPI(Resource):
    '''
    Countries Indicator element URI
    Methods: GET, PUT, DELETE
    '''

    def get(self, id, indicator_id):
        '''
        Show indicator
        Response 200 OK
        '''
        datasets = datasource_service.get_by_code(id).datasets
        indicator = None
        for dataset in datasets:
            for indicator in dataset.indicators:
                if indicator.id == indicator_id:
                    indicator = dataset.indicator
        if indicator is None:
            abort(404)
        if is_xml_accepted(request):
            return Response(xml_converter.object_to_xml(indicator,
                                                        'indicator'), mimetype='application/xml')
        else:
            return Response(json_converter.object_to_json(indicator
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
api.add_resource(CountriesIndicatorListAPI, '/api/countries/<iso3>/indicators', endpoint='countries_indicators_list')
api.add_resource(CountriesIndicatorAPI, '/api/countries/<iso3>/indicators/<indicator_id>', endpoint='countries_indicators')
api.add_resource(ObservationListAPI, '/api/observations', endpoint='observations_list')
api.add_resource(ObservationAPI, '/api/observations/<id>', endpoint='observations')
api.add_resource(RegionListAPI, '/api/regions', endpoint='regions_list')
api.add_resource(RegionAPI, '/api/regions/<id>', endpoint='regions')
api.add_resource(RegionsCountryListAPI, '/api/regions/<id>/countries', endpoint='regions_countries_list')
api.add_resource(RegionsCountryAPI, '/api/regions/<id>/countries/<iso3>', endpoint='regions_countries')
api.add_resource(DataSourceListAPI, '/api/datasources', endpoint='datasources_list')
api.add_resource(DataSourceAPI, '/api/datasources/<id>', endpoint='datasources')
api.add_resource(DatasetListAPI, '/api/datasets', endpoint='datasets_list')
api.add_resource(DatasetAPI, '/api/datasets/<id>', endpoint='datasets')
api.add_resource(DataSourceIndicatorListAPI, '/api/datasources/<id>/indicators', endpoint='datasources_indicators_list')
api.add_resource(DataSourceIndicatorAPI, '/api/datasources/<id>/indicators/<indicator_id>', endpoint='datasources_indicators')


def is_xml_accepted(request):
    '''
    Returns if json is accepted or not, returns json as default
    '''
    return request.args.get('format') == "xml"
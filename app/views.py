"""
Created on 03/02/2014

:author: Weso
"""
from flask_restful import Resource, abort, Api
from flask.wrappers import Response
from flask.helpers import url_for
from flask import json, render_template
from app import app, cache
from app.utils import JSONConverter, XMLConverter, CSVConverter, DictionaryList2ObjectList
from model.models import Country, Indicator, User, Organization, Observation, Region, DataSource, Dataset, Value, \
    Topic, Instant, Interval, RegionTranslation, IndicatorTranslation, TopicTranslation, YearInterval, Time, \
    MeasurementUnit, Auth
from app.services import CountryService, IndicatorService, UserService, OrganizationService, ObservationService, \
    RegionService, DataSourceService, DatasetService, ValueService, TopicService, IndicatorRelationshipService, \
    RegionTranslationService, IndicatorTranslationService, TopicTranslationService, MeasurementUnitService, AuthService
from flask import request, redirect
from datetime import datetime
from functools import wraps


api = Api(app)
country_service = CountryService()
indicator_service = IndicatorService()
user_service = UserService()
organization_service = OrganizationService()
observation_service = ObservationService()
region_service = RegionService()
datasource_service = DataSourceService()
dataset_service = DatasetService()
value_service = ValueService()
topic_service = TopicService()
indicator_relationship_service = IndicatorRelationshipService()
region_translation_service = RegionTranslationService()
indicator_translation_service = IndicatorTranslationService()
topic_translation_service = TopicTranslationService()
auth_service = AuthService()
measurement_unit_service = MeasurementUnitService()
json_converter = JSONConverter()
xml_converter = XMLConverter()
csv_converter = CSVConverter()
list_converter = DictionaryList2ObjectList()


def localhost_decorator(f):
    """
    Decorator that allows connections only from localhost, if not
    it will return a 403 FORBIDDEN error code
    """
    def call(*args, **kwargs):
        if request.remote_addr == '127.0.0.1' or request.remote_addr == 'localhost':
            return f(*args, **kwargs)
        else:
            abort(403)
    return call


def check_auth(username, password):
    """
    This function is called to check if a username /
    password combination is valid.
    """
    auth = auth_service.get_by_code(username)
    if auth is None:
        return False
    return password == auth.token


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if (not auth or not check_auth(auth.username, auth.password)) \
                and (not request.remote_addr == '127.0.0.1' and not request.remote_addr == 'localhost'):
            return authenticate()
        if auth:
            app.logger.info("Request from user: " + auth.username)
        return f(*args, **kwargs)
    return decorated


def make_cache_key(*args, **kwargs):
    """
    Function that allows creating a unique id for every request
    There was a problem caching and changing arguments of the URL, so this is one possible solution
    :see: http://stackoverflow.com/questions/9413566/flask-cache-memoize-url-query-string-parameters-as-well
    """
    return request.url


class CountryListAPI(Resource):
    """
    Countries collection URI
    Methods: GET, POST, PUT, DELETE
    """
    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all countries
        Response 200 OK
        """
        countries = country_service.get_all()
        translate_region_list(countries)
        return response_xml_or_json_list(request, countries, 'countries', 'country')

    @localhost_decorator
    def post(self):
        """
        Create a new country
        Response 201 CREATED
        :return: URI
        """
        country = Country(request.json.get("iso2"), request.json.get("iso3"), request.json.get("faoURI"))
        country.is_part_of_id = request.json.get("is_part_of_id")
        country.un_code = request.json.get("un_code")
        if country.iso2 is not None and country.iso3 is not None:
            country_service.insert(country)
            return {'URI': url_for('countries', code=country.iso3)}, 201  # returns the URI for the new country
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all countries given
        Response 204 NO CONTENT
        """
        country_list = json.loads(request.data)
        country_list = list_converter.convert(country_list)
        country_service.update_all(country_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all countries
        Response 204 NO CONTENT
        :attention: Take care of what you do, all countries will be destroyed
        """
        country_service.delete_all()
        return {}, 204


class CountryAPI(Resource):
    """
    Countries element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, code):
        """
        Show country
        Response 200 OK
        """
        country = country_service.get_by_code(code)
        if country is None:
            abort(404)
        translate_region(country)
        country.region = region_service.get_by_artificial_code(country.is_part_of_id)
        if not hasattr(country, 'other_parseable_fields'):
            country.other_parseable_fields = []
        country.other_parseable_fields.append('region')
        if country.region is not None:
            translate_region(country.region)
        return response_xml_or_json_item(request, country, 'country')

    @localhost_decorator
    def put(self, code):
        """
        If exists update country
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        country = country_service.get_by_code(code)
        if country is not None:
            country.iso2 = request.json.get("iso2")
            country.fao_URI = request.json.get("faoURI")
            country.name = request.json.get("name")
            country_service.update(country)
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, code):
        """
        Delete country
        Response 204 NO CONTENT
        """
        country_service.delete(code)
        return {}, 204


class IndicatorListAPI(Resource):
    """
    Indicators collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all indicators
        Response 200 OK
        """
        indicators = indicator_service.get_all()
        translate_indicator_list(indicators)
        return response_xml_or_json_list(request, indicators, 'indicators', 'indicator')

    @localhost_decorator
    def post(self):
        """
        Create a new indicator
        Response 201 CREATED
        :return: URI
        """
        indicator = Indicator(request.json.get("id"), request.json.get("preferable_tendency"),
                              request.json.get("measurement_unit_id"), request.json.get("dataset_id"),
                              request.json.get("compound_indicator_id"), request.json.get("starred"))
        indicator.type = request.json.get("type")
        indicator.topic_id = request.json.get("topic_id")
        indicator.preferable_tendency = request.json.get("preferable_tendency")
        if request.json.get("last_update") is not None:
            indicator.last_update = datetime.fromtimestamp(long(request.json.get("last_update")))
        if indicator.id is not None:
            indicator_service.insert(indicator)
            return {'URI': url_for('indicators', id=indicator.id)}, 201  # returns the URI for the new indicator
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all indicators given
        Response 204 NO CONTENT
        """
        indicator_list = json.loads(request.data)
        indicator_list = list_converter.convert(indicator_list)
        indicator_service.update_all(indicator_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all indicators
        Response 204 NO CONTENT
        :attention: Take care of what you do, all indicators will be destroyed
        """
        indicator_service.delete_all()
        return {}, 204


class IndicatorAPI(Resource):
    """
    Indicators element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show indicator
        Response 200 OK
        """
        indicator = indicator_service.get_by_code(id)
        if indicator is None:
            abort(404)
        translate_indicator(indicator)
        return response_xml_or_json_item(request, indicator, 'indicator')

    @localhost_decorator
    def put(self, id):
        """
        If exists update indicator
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
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

    @localhost_decorator
    def delete(self, id):
        """
        Delete indicators
        Response 204 NO CONTENT
        """
        indicator_service.delete(id)
        return {}, 204


class IndicatorTopAPI(Resource):
    """
    Indicator top api
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show top 10 countries with the highest value for a given indicator
        Response 200 OK
        """
        countries, top = filter_by_region_and_top(id)
        output = []
        for i in range(len(countries)):
            element = EmptyObject()
            element.iso3 = countries[i].iso3
            element.value_id = top[i].id
            output.append(element)
        return response_xml_or_json_list(request, output, 'tops', 'top')


class IndicatorAverageAPI(Resource):
    """
    Indicator average api
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show the average value for a indicator of all countries
        Response 200 OK
        """
        top = filter_by_region_and_top(id)[1]
        average = observations_average(top)
        element = EmptyObject()
        element.value = average
        return response_xml_or_json_item(request, element, 'average')


class IndicatorCompatibleAPI(Resource):
    """
    Indicator compatible api
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show the compatible indicators of the given indicator
        Response 200 OK
        """
        indicator = indicator_service.get_by_code(id)
        indicators = indicator_service.get_all()
        compatibles = [ind for ind in indicators
                       if indicator.measurement_unit_id == ind.measurement_unit_id
                        and ind is not indicator]
        translate_indicator_list(compatibles)
        return response_xml_or_json_list(request, compatibles, 'indicators', 'indicator')


class IndicatorStarredAPI(Resource):
    """
    Indicators starred URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List starred indicators
        Response 200 OK
        """
        indicators = indicator_service.get_all()
        indicators = filter(lambda i: i.starred, indicators)
        translate_indicator_list(indicators)
        return response_xml_or_json_list(request, indicators, 'indicators', 'indicator')


class UserListAPI(Resource):
    """
    Users collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all users
        Response 200 OK
        """
        return response_xml_or_json_list(request, user_service.get_all(), 'users', 'user')

    @localhost_decorator
    def post(self):
        """
        Create a new user
        Response 201 CREATED
        :return: URI
        """
        user = User(request.json.get("id"), request.json.get("ip"),
                    request.json.get("timestamp"), request.json.get("organization_id"))
        if user.id is not None:
            user_service.insert(user)
            return {'URI': url_for('users', id=user.id)}, 201  # returns the URI for the new user
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all users given
        Response 204 NO CONTENT
        """
        user_list = json.loads(request.data)
        user_list = list_converter.convert(user_list)
        user_service.update_all(user_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all users
        Response 204 NO CONTENT
        :attention: Take care of what you do, all users will be destroyed
        """
        user_service.delete_all()
        return {}, 204


class UserAPI(Resource):
    """
    Users element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show user
        Response 200 OK
        """
        user = user_service.get_by_code(id)
        if user is None:
            abort(404)
        return response_xml_or_json_item(request, user, 'user')

    @localhost_decorator
    def put(self, id):
        """
        If exists update user
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
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

    @localhost_decorator
    def delete(self, id):
        """
        Delete user
        Response 204 NO CONTENT
        """
        user_service.delete(id)
        return {}, 204


class OrganizationListAPI(Resource):
    """
    Organizations collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all organizations
        Response 200 OK
        """
        return response_xml_or_json_list(request, organization_service.get_all(), 'organizations', 'organization')

    @localhost_decorator
    def post(self):
        """
        Create a new organization
        Response 201 CREATED
        :return: URI
        """
        organization = Organization(request.json.get("id"), request.json.get("name"))
        organization.is_part_of_id = request.json.get("is_part_of_id")
        organization.url = request.json.get("url")
        if organization.id is not None:
            organization_service.insert(organization)
            return {'URI': url_for('organizations', id=organization.id)}, 201  # returns the URI for the new user
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all organizations given
        Response 204 NO CONTENT
        """
        organization_list = json.loads(request.data)
        organization_list = list_converter.convert(organization_list)
        organization_service.update_all(organization_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all organizations
        Response 204 NO CONTENT
        @attention: Take care of what you do, all organizations will be destroyed
        """
        organization_service.delete_all()
        return {}, 204


class OrganizationAPI(Resource):
    """
    Organizations element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show organization
        Response 200 OK
        """
        organization = organization_service.get_by_code(id)
        if organization is None:
            abort(404)
        return response_xml_or_json_item(request, organization, 'organization')

    @localhost_decorator
    def put(self, id):
        """
        If exists update organization
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
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

    @localhost_decorator
    def delete(self, id):
        """
        Delete organization
        Response 204 NO CONTENT
        """
        organization_service.delete(id)
        return {}, 204


class OrganizationUserListAPI(Resource):
    """
    Organizations users collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, organization_id):
        """
        List all users of a given organization
        Response 200 OK
        """
        return response_xml_or_json_list(request, organization_service.get_by_code(organization_id).users, 'users', 'user')


class OrganizationUserAPI(Resource):
    """
    Organizations users element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, organization_id, user_id):
        """
        Show a user by its organization id and its user id
        If found Response 200 OK
        Else Response 404 NOT FOUND
        """
        selected_user = None
        for user in organization_service.get_by_code(organization_id).users:
            if user.id == user_id:
                selected_user = user
        if selected_user is None:
            abort(404)
        return response_xml_or_json_item(request, selected_user, 'user')


class CountriesIndicatorListAPI(Resource):
    """
    Countries Indicator collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, iso3):
        """
        List all indicators of a given country
        Response 200 OK
        """
        observations = country_service.get_by_code(iso3).observations
        indicators = []
        for obs in observations:
            if obs.indicator is not None:
                indicators.append(obs.indicator)
        set_indicators = set(indicators)
        indicators = list(set_indicators)
        translate_indicator_list(indicators)
        return response_xml_or_json_list(request, indicators, 'indicators', 'indicator')


class CountriesIndicatorAPI(Resource):
    """
    Countries Indicator element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, iso3, indicator_id):
        """
        Show a indicators by its country id and its indicator id
        If found Response 200 OK
        Else Response 404 NOT FOUND
        """
        observations = country_service.get_by_code(iso3).observations
        indicator = None
        for obs in observations:
            if obs.indicator is not None and obs.indicator.id == indicator_id:
                indicator = obs.indicator
        if indicator is None:
            abort(404)
        translate_indicator(indicator)
        return response_xml_or_json_item(request, indicator, 'indicator')


class ObservationListAPI(Resource):
    """
    Observations collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @localhost_decorator
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all observations
        Response 200 OK
        """
        return response_xml_or_json_list(request, observation_service.get_all(), 'observations', 'observation')

    @localhost_decorator
    def post(self):
        """
        Create a new observation
        Response 201 CREATED
        :return: URI
        """
        observation = Observation(request.json.get("id"))
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
            observation_service.insert(observation)
            return {'URI': url_for('observations', id=observation.id)}, 201  # returns the URI for the new user
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all observations given
        Response 204 NO CONTENT
        """
        observation_list = json.loads(request.data)
        observation_list = list_converter.convert(observation_list)
        observation_service.update_all(observation_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all observations
        Response 204 NO CONTENT
        :attention: Take care of what you do, all observations will be destroyed
        """
        observation_service.delete_all()
        return {}, 204


class ObservationAPI(Resource):
    """
    Observations element URI
    Methods: GET, PUT, DELETE
    """

    @localhost_decorator
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show observations
        Response 200 OK
        """
        if country_service.get_by_code(id) is not None:
            country = country_service.get_by_code(id)
            return response_xml_or_json_list(request, country.observations, 'observations', 'observation')
        elif indicator_service.get_by_code(id) is not None:
            observations = []
            indicator = indicator_service.get_by_code(id)
            for dataset in indicator.datasets:
                observations.extend(dataset.observations)
            return response_xml_or_json_list(request, observations, 'observations', 'observation')
        elif region_service.get_by_code(id) is not None:
            region = region_service.get_by_code(id)
            observations = []
            for country in country_service.get_all():
                if country.is_part_of_id is region.id:
                    observations.extend(country.observations)
            return response_xml_or_json_list(request, observations, 'observations', 'observation')
        else:
            response = observation_service.get_by_code(id)
            if response is None:
                abort(404)
            return response_xml_or_json_item(request, response, 'observation')

    @localhost_decorator
    def put(self, id):
        """
        If exists update observation
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        observation = observation_service.get_by_code(id)
        if observation is not None:
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

    @localhost_decorator
    def delete(self, id):
        """
        Delete observation
        Response 204 NO CONTENT
        """
        observation_service.delete(id)
        return {}, 204


class RegionListAPI(Resource):
    """
    Regions collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all region
        Response 200 OK
        """
        regions = region_service.get_all()
        translate_region_list(regions)
        return response_xml_or_json_list(request, regions, 'regions', 'region')

    @localhost_decorator
    def post(self):
        """
        Create a new region
        Response 201 CREATED
        :return: URI
        """
        region = Region()
        region.id = request.json.get("name")
        region.id = request.json.get("id")
        region.is_part_of_id = request.json.get("is_part_of_id")
        region.un_code = request.json.get("un_code")
        if region.un_code is not None:
            region_service.insert(region)
            return {'URI': url_for('regions', id=region.id)}, 201 #returns the URI for the new region
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all regions given
        Response 204 NO CONTENT
        """
        region_list = json.loads(request.data)
        region_list = list_converter.convert(region_list)
        region_service.update_all(region_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all regions
        Response 204 NO CONTENT
        :attention: Take care of what you do, all regions will be destroyed
        """
        region_service.delete_all()
        return {}, 204


class RegionAPI(Resource):
    """
    Regions element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show region
        Response 200 OK
        """
        region = region_service.get_by_code(id)
        if region is None:
            abort(404)
        translate_region(region)
        return response_xml_or_json_item(request, region, 'region')

    @localhost_decorator
    def put(self, id):
        """
        If exists update region
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        region = region_service.get_by_code(id)
        if region is not None:
            region.is_part_of_id = request.json.get("is_part_of_id")
            region_service.update(region)
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, id):
        """
        Delete region
        Response 204 NO CONTENT
        """
        region_service.delete(id)
        return {}, 204


class RegionsCountryListAPI(Resource):
    """
    Regions Country collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        List all countries of a given region
        Response 200 OK
        """
        region = region_service.get_by_code(id)
        countries = []
        if region is not None and region.id == 1:
            countries = country_service.get_all()
        else:
            for country in country_service.get_all():
                if country.is_part_of_id == region.id:
                    countries.append(country)
        translate_region_list(countries)
        return response_xml_or_json_list(request, countries, 'countries', 'country')


class RegionsRegionListAPI(Resource):
    """
    Regions Region collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        List all regions of a given region
        Response 200 OK
        """
        regions = get_regions_of_region(id)
        return response_xml_or_json_list(request, regions, 'regions', 'region')


class RegionsCountryAPI(Resource):
    """
    Countries Indicator element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id, iso3):
        """
        Show country by its region id and its country id
        Response 200 OK
        """
        region = region_service.get_by_code(id)
        selected_country = None
        for country in country_service.get_all():
            if country.is_part_of_id == region.id and country.iso3 == iso3:
                selected_country = country
        if selected_country is None:
            abort(404)
        translate_region(selected_country)
        return response_xml_or_json_item(request, selected_country, 'country')


class DataSourceListAPI(Resource):
    """
    DataSource collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all datasources
        Response 200 OK
        """
        return response_xml_or_json_list(request, datasource_service.get_all(), 'datasources', 'datasource')

    @localhost_decorator
    def post(self):
        """
        Create a new datasource
        Response 201 CREATED
        :return: URI
        """
        datasource = DataSource(request.json.get("name"))
        datasource.id = request.json.get("id")
        datasource.organization_id = request.json.get("organization_id")
        if datasource.id is not None:
            datasource_service.insert(datasource)
            return {'URI': url_for('datasources', id=datasource.id)}, 201 #returns the URI for the new datasource
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all datasources given
        Response 204 NO CONTENT
        """
        datasource_list = json.loads(request.data)
        datasource_list = list_converter.convert(datasource_list)
        datasource_service.update_all(datasource_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all datasources
        Response 204 NO CONTENT
        :attention: Take care of what you do, all datasources will be destroyed
        """
        datasource_service.delete_all()
        return {}, 204


class DataSourceAPI(Resource):
    """
    Datasources element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show datasource
        Response 200 OK
        """
        datasource = datasource_service.get_by_code(id)
        if datasource is None:
            abort(404)
        return response_xml_or_json_item(request, datasource, 'datasource')

    @localhost_decorator
    def put(self, id):
        """
        If exists update datasource
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        datasource = datasource_service.get_by_code(id)
        if datasource is not None:
            datasource.id_source = request.json.get("id_source")
            datasource.name = request.json.get("name")
            datasource.organization_id = request.json.get("organization_id")
            datasource_service.update(datasource)
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, id):
        """
        Delete datasource
        Response 204 NO CONTENT
        """
        datasource_service.delete(id)
        return {}, 204


class DatasetListAPI(Resource):
    """
    Dataset collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all datasets
        Response 200 OK
        """
        return response_xml_or_json_list(request, dataset_service.get_all(), 'datasets', 'dataset')

    @localhost_decorator
    def post(self):
        """
        Create a new dataset
        Response 201 CREATED
        :return: URI
        """
        dataset = Dataset(request.json.get("id"))
        dataset.sdmx_frequency = request.json.get("sdmx_frequency")
        dataset.datasource_id = request.json.get("datasource_id")
        dataset.license_id = request.json.get("license_id")
        dataset.indicators_id = request.json.get("indicators_id")
        if dataset.id is not None:
            dataset_service.insert(dataset)
            return {'URI': url_for('datasets', id=dataset.id)}, 201 #returns the URI for the new dataset
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all datasets given
        Response 204 NO CONTENT
        """
        dataset_list = json.loads(request.data)
        dataset_list = list_converter.convert(dataset_list)
        dataset_service.update_all(dataset_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all datasets
        Response 204 NO CONTENT
        :attention: Take care of what you do, all datasets will be destroyed
        """
        dataset_service.delete_all()
        return {}, 204


class DatasetAPI(Resource):
    """
    Dataset element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show dataset
        Response 200 OK
        """
        dataset = dataset_service.get_by_code(id)
        if dataset is None:
            abort(404)
        return response_xml_or_json_item(request, dataset, 'dataset')

    @localhost_decorator
    def put(self, id):
        """
        If exists update dataset
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        dataset = dataset_service.get_by_code(id)
        if dataset is not None:
            dataset.sdmx_frequency = request.json.get("sdmx_frequency")
            dataset.datasource_id = request.json.get("datasource_id")
            dataset.license_id = request.json.get("license_id")
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, id):
        """
        Delete dataset
        Response 204 NO CONTENT
        """
        dataset_service.delete(id)
        return {}, 204


class DataSourceIndicatorListAPI(Resource):
    """
    DataSource Indicator collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        List all indicators of a given datasource
        Response 200 OK
        """
        datasets = datasource_service.get_by_code(id).datasets
        indicators = []
        for dataset in datasets:
            indicators.extend(dataset.indicators)
        translate_indicator_list(indicators)
        return response_xml_or_json_list(request, indicators, 'indicators', 'indicator')


class DataSourceIndicatorAPI(Resource):
    """
    Datasource Indicator element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id, indicator_id):
        """
        Show indicator by its datasource id and indicator id
        Response 200 OK
        """
        datasets = datasource_service.get_by_code(id).datasets
        indicator = None
        for dataset in datasets:
            for ind in dataset.indicators:
                if ind.id == indicator_id:
                    indicator = ind
        if indicator is None:
            abort(404)
        translate_indicator(indicator)
        return response_xml_or_json_item(request, indicator, 'indicator')


class ObservationByTwoAPI(Resource):
    """
    Observation by two collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id_first_filter, id_second_filter):
        """
        Show observations filtering by two ids.
        It could be one of three next:
         * Indicator id and country iso3
         * Country iso3 and indicator id
         * Region un_code and indicator id
        :param id_first_filter: first filter
        :param id_second_filter: second filter
        Response 200 OK
        """

        observations = get_observations_by_two_filters(id_first_filter, id_second_filter)
        if observations is not None:
            return response_xml_or_json_list(request, observations, 'observations', 'observation')
        abort(400)


class ObservationByCountryStarred(Resource):
    """
    Observation by country and starred indicator collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, iso3):
        """
        Show observations filtering by country and showed if the indicator is starred.
        :param iso3: iso3 of the country to filter
        Response 200 OK
        """
        country = country_service.get_by_code(iso3)
        translate_region(country)
        if country is None:
            abort(404)
        observations = [obs for obs in country.observations if obs.indicator.starred]
        for observation in observations:
            observation.country = country
            indicator = indicator_service.get_by_code(observation.indicator.id)
            translate_indicator(indicator)
            observation.indicator = indicator
            observation.measurement_unit = indicator.measurement_unit
            observation.other_parseable_fields = ['country', 'indicator', 'ref_time', 'value', 'measurement_unit']
        if observations is not None:
            return response_xml_or_json_list(request, observations, 'observations', 'observation')
        abort(400)


class ObservationByTwoAverageAPI(Resource):
    """
    Observations by two average URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id_first_filter, id_second_filter):
        """
        Show observations average filtering by two ids.
        It could be one of three next:
         * Indicator id and country iso3
         * Country iso3 and indicator id
         * Region un_code and indicator id
        :param id_first_filter: first filter
        :param id_second_filter: second filter
        Response 200 OK
        """

        observations = get_observations_by_two_filters(id_first_filter, id_second_filter)
        if observations is not None:
            averages = []
            all_observations_average = EmptyObject()
            all_observations_average.time = 'all'
            all_observations_average.average = observations_average(observations)
            averages.append(all_observations_average)
            observations_times = [observation.ref_time.value for observation in observations]
            observations_times = list(set(observations_times))
            observations_times.sort()
            for observation_time in observations_times:
                grouped_observations = filter(lambda obs: obs.ref_time.value == observation_time, observations)
                grouped_observations = [observation for observation in grouped_observations if observation.value.value is not None]
                if len(grouped_observations) > 0:
                    average_time = EmptyObject()
                    average_time.time = observation_time
                    average_time.average = reduce(lambda x, y: x + float(y.value.value), grouped_observations, 0) / len(grouped_observations)
                    averages.append(average_time)
            return response_xml_or_json_list(request, averages, 'averages', 'average')
        abort(400)


def get_observations_by_two_filters(id_first_filter, id_second_filter):
    """
    Return observations filtering by two ids.
    It could be one of three next:
     * Indicator id and country iso3
     * Country iso3 and indicator id
     * Region un_code and indicator id
    :param id_first_filter: id of the first filter
    :param id_second_filter: id of the second filter
    :return: Filtered observations
    """
    def append_objects():
        """
        Appends some neested object to main object, in order to be showed on the output
        """
        translate_region(country)
        translate_indicator(indicator)
        for observation in observations:
            observation.country = country
            observation.indicator = indicator
            observation.ref_time = observation.ref_time
            observation.measurement_unit = indicator.measurement_unit
            observation.other_parseable_fields = ['country', 'indicator', 'ref_time', 'value', 'measurement_unit']

    observations = None
    if country_service.get_by_code(id_first_filter) and indicator_service.get_by_code(id_second_filter):
            country = country_service.get_by_code(id_first_filter)
            indicator = indicator_service.get_by_code(id_second_filter)
            observations = [observation for observation in country.observations
                            if observation.indicator_id == id_second_filter]
            append_objects()
    elif indicator_service.get_by_code(id_first_filter) and country_service.get_by_code(id_second_filter):
        country = country_service.get_by_code(id_second_filter)
        indicator = indicator_service.get_by_code(id_first_filter)
        observations = [observation for observation in country.observations
                        if observation.indicator_id == id_first_filter]
        append_objects()
    elif region_service.get_by_code(id_first_filter) and indicator_service.get_by_code(id_second_filter):
        observations = []
        region = region_service.get_by_code(id_first_filter)
        indicator = indicator_service.get_by_code(id_second_filter)
        translate_indicator(indicator)
        for country in country_service.get_all():
            if country.is_part_of_id == region.id or region.id == 1:
                country_observations = country.observations
                for observation in country_observations:
                    if observation.indicator_id == id_second_filter:
                        observation.country = country
                        translate_region(country)
                        observation.indicator = indicator
                        observation.ref_time = observation.ref_time
                        observation.measurement_unit = indicator.measurement_unit
                        observation.other_parseable_fields = ['country', 'indicator', 'ref_time', 'value', 'measurement_unit']
                        observations.append(observation)
    if observations is not None and len(observations) > 0 and observations[0].ref_time is not None and isinstance(observations[0].ref_time, Time):
        observations.sort(key=lambda obs: get_intervals([obs.ref_time])[0])
        for observation in observations:
            observations_country = filter(lambda obs: obs.region_id == observation.region_id, observations)
            for j in range(len(observations_country)):
                if observation == observations_country[j]:
                    if j == 0 or observation.value.value is None or observations_country[j-1].value.value:
                        observation.tendency = -2
                    elif float(observation.value.value) == float(observations_country[j-1].value.value):
                        observation.tendency = 0
                    elif float(observations_country[j-1].value.value) > float(observation.value.value):
                        observation.tendency = -1
                    elif float(observations_country[j-1].value.value) < float(observation.value.value):
                        observation.tendency = 1
                    observation.other_parseable_fields.append('tendency')
    return observations if observations is not None else []


class ValueListAPI(Resource):
    """
    Value collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all values
        Response 200 OK
        """
        return response_xml_or_json_list(request, value_service.get_all(), 'values', 'value')

    @localhost_decorator
    def post(self):
        """
        Create a new value
        Response 201 CREATED
        :return: URI
        """
        value = Value()
        value.id = request.json.get("id")
        value.obs_status = request.json.get("obs_status")
        value.value_type = request.json.get("value_type")
        value.value = request.json.get("value")
        if value.value is not None:
            value_service.insert(value)
            return {'URI': url_for('values', id=value.id)}, 201  # returns the URI for the new dataset
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all values given
        Response 204 NO CONTENT
        """
        value_list = json.loads(request.data)
        value_list = list_converter.convert(value_list)
        value_service.update_all(value_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all value
        Response 204 NO CONTENT
        :attention: Take care of what you do, all values will be destroyed
        """
        value_service.delete_all()
        return {}, 204


class ValueAPI(Resource):
    """
    Value element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show value
        Response 200 OK
        """
        value = value_service.get_by_code(id)
        if value is None:
            abort(404)
        return response_xml_or_json_item(request, value, 'value')

    @localhost_decorator
    def put(self, id):
        """
        If exists update value
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        value = value_service.get_by_code(id)
        if value is not None:
            value.id = request.json.get("id")
            value.obs_status = request.json.get("obs_status")
            value.value_type = request.json.get("value_type")
            value.value = request.json.get("value")
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, id):
        """
        Delete value
        Response 204 NO CONTENT
        """
        value_service.delete(id)
        return {}, 204


class TopicListAPI(Resource):
    """
    Topic collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all topics
        Response 200 OK
        """
        topics = topic_service.get_all()
        translate_topic_list(topics)
        return response_xml_or_json_list(request, topics, 'topics', 'topic')

    @localhost_decorator
    def post(self):
        """
        Create a new topic
        Response 201 CREATED
        :return: URI
        """
        topic = Topic(request.json.get("id"))
        if topic.id is not None:
            topic_service.insert(topic)
            return {'URI': url_for('topics', id=topic.id)}, 201  # returns the URI for the new dataset
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all topics given
        Response 204 NO CONTENT
        """
        topic_list = json.loads(request.data)
        topic_list = list_converter.convert(topic_list)
        topic_service.update_all(topic_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all topics
        Response 204 NO CONTENT
        :attention: Take care of what you do, all topic will be destroyed
        """
        topic_service.delete_all()
        return {}, 204


class TopicAPI(Resource):
    """
    Topic element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show topic
        Response 200 OK
        """
        topic = topic_service.get_by_code(id)
        if topic is None:
            abort(404)
        translate_topic(topic)
        return response_xml_or_json_item(request, topic, 'topic')

    @localhost_decorator
    def put(self, id):
        """
        If exists update topic
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        topic = topic_service.get_by_code(id)
        if topic is not None:
            topic.id = request.json.get("id")
            topic.name = request.json.get("name")
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, id):
        """
        Delete topic
        Response 204 NO CONTENT
        """
        topic_service.delete(id)
        return {}, 204


class MeasurementUnitListAPI(Resource):
    """
    Measurement unit collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all measurement untis
        Response 200 OK
        """
        measurement_units = measurement_unit_service.get_all()
        return response_xml_or_json_list(request, measurement_units, 'measurement_units', 'measurement_unit')

    @localhost_decorator
    def post(self):
        """
        Create a new measurement_unit
        Response 201 CREATED
        :return: URI
        """
        measurement_unit = MeasurementUnit(request.json.get('id'), request.json.get('name'),
                                           request.json.get('convertible_to'), request.json.get('factor'))
        if measurement_unit.id is not None:
            measurement_unit_service.insert(measurement_unit)
            return {'URI': url_for('measurement_unit', id=measurement_unit.id)}, 201  # returns the URI for the new dataset
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all measurement_units given
        Response 204 NO CONTENT
        """
        measurement_unit_list = json.loads(request.data)
        measurement_unit_list = list_converter.convert(measurement_unit_list)
        measurement_unit_service.update_all(measurement_unit_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all measurement_untis
        Response 204 NO CONTENT
        :attention: Take care of what you do, all measurement_units will be destroyed
        """
        measurement_unit_service.delete_all()
        return {}, 204


class MeasurementUnitAPI(Resource):
    """
    Measurement unit element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show measurement unit
        Response 200 OK
        """
        measurement_unit = measurement_unit_service.get_by_code(id)
        if measurement_unit is None:
            abort(404)
        return response_xml_or_json_item(request, measurement_unit, 'measurement_unit')

    @localhost_decorator
    def put(self, id):
        """
        If exists update measurement_unit
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        measurement_unit = measurement_unit_service.get_by_code(id)
        if measurement_unit is not None:
            measurement_unit.id = request.json.get("id")
            measurement_unit.name = request.json.get("name")
            measurement_unit.convertible_to = request.json.get("convertible_to")
            measurement_unit.factor = request.json.get("factor")
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, id):
        """
        Delete measurement_unit
        Response 204 NO CONTENT
        """
        measurement_unit_service.delete(id)
        return {}, 204


class TopicIndicatorListAPI(Resource):
    """
    Topics Indicator collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, topic_id):
        """
        List all indicators by a given topic
        Response 200 OK
        """
        indicators = topic_service.get_by_code(topic_id).indicators
        translate_indicator_list(indicators)
        return response_xml_or_json_list(request, indicators, 'indicators', 'indicator')


class TopicIndicatorAPI(Resource):
    """
    Topics Indicator element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, topic_id, indicator_id):
        """
        Show indicators by its topic id and indicator id
        Response 200 OK
        """
        selected_indicator = None
        for indicator in topic_service.get_by_code(topic_id).indicators:
            if indicator.id == indicator_id:
                selected_indicator = indicator
        if selected_indicator is None:
            abort(404)
        translate_indicator(selected_indicator)
        return response_xml_or_json_item(request, selected_indicator, 'indicator')


class RegionCountriesWithDataAPI(Resource):
    """
    Countries with data by region element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, region_id):
        """
        Show country that have some observations by a given region (country is_part_of region)
        Response 200 OK
        """
        region = region_service.get_by_code(region_id)
        countries = [country for country in country_service.get_all() if country.is_part_of_id == region.id]
        countries = [country for country in countries if len(country.observations) > 0]
        translate_region_list(countries)
        return response_xml_or_json_list(request, countries, 'countries', 'country')


class CountriesIndicatorLastUpdateAPI(Resource):
    """
    More recent indicators of a country collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, iso3):
        """
        Show indicators last_update by a given country
        Response 200 OK
        """
        indicators = [observation.indicator for observation in country_service.get_by_code(iso3).observations]
        indicator = max(indicators, key=lambda ind: ind.last_update)
        result = EmptyObject()
        result.last_update = indicator.last_update
        return response_xml_or_json_item(request, result, 'last_update')


class IndicatorsCountryLastUpdateAPI(Resource):
    """
    More recent indicator of a country element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id, iso3):
        """
        Show indicator last_update by its country id and indicator id
        Response 200 OK
        """
        observations = country_service.get_by_code(iso3).observations
        indicator = (observation.indicator for observation in observations if observation.indicator.id == id).next()
        result = EmptyObject()
        result.last_update = indicator.last_update
        return response_xml_or_json_item(request, result, 'last_update')


class ObservationByPeriodAPI(Resource):
    """
    Observations by period element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show observations of one of this given as parameter:
        * Country as iso3
        * Indicator as indicator id
        * Region as un_code
        Observations will be filtered between two dates, if they are not supplied
        whole range will be returned
        Response 200 OK
        """
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        from_date, to_date = str_date_to_date(date_from, date_to)
        if country_service.get_by_code(id) is not None:
            country = country_service.get_by_code(id)
            observations = filter_observations_by_date_range(country.observations, from_date, to_date)
            return response_xml_or_json_list(request, observations, 'observations', 'observation')
        elif indicator_service.get_by_code(id) is not None:
            observations = []
            indicator = indicator_service.get_by_code(id)
            for dataset in indicator.datasets:
                observations.extend(dataset.observations)
            observations = filter_observations_by_date_range(observations, from_date, to_date)
            return response_xml_or_json_list(request, observations, 'observations', 'observation')
        elif region_service.get_by_code(id) is not None:
            region = region_service.get_by_code(id)
            observations = []
            for country in country_service.get_all():
                if country.is_part_of_id == region.id:
                    observations.extend(country.observations)
            observations = filter_observations_by_date_range(observations, from_date, to_date)
            return response_xml_or_json_list(request, observations, 'observations', 'observation')
        else:
            response = observation_service.get_by_code(id)
            if response is None:
                abort(404)
            return response_xml_or_json_item(request, response, 'observation')


class IndicatorByPeriodAPI(Resource):
    """
    Indicator by period element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show observations by its given indicator
        Observations will be filtered between two dates, if they are not supplied
        whole range will be returned
        Response 200 OK
        """
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        from_date, to_date = str_date_to_date(date_from, date_to)
        if indicator_service.get_by_code(id) is not None:
            observations = observation_service.get_all()
            observations = [obs for obs in observations if obs.indicator_id == id]
            observations = filter_observations_by_date_range(observations, from_date, to_date)
        else:
            abort(404)
        return response_xml_or_json_list(request, observations, 'observations', 'observation')


class IndicatorRegionsWithDataAPI(Resource):
    """
    Indicator by period element URI
    Methods: GET
    """
    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show regions with data for the given indicator
        Response 200 OK
        """
        if indicator_service.get_by_code(id) is not None:
            regions_with_data = get_regions_with_data(id)
        else:
            abort(404)
        return response_xml_or_json_list(request, regions_with_data, 'regions', 'region')


class IndicatorRegionsWihtoutDataAPI(Resource):
    """
    Indicator regions without data element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show observations by its given indicator
        Observations will be filtered between two dates, if they are not supplied
        whole range will be returned
        Response 200 OK
        """
        if indicator_service.get_by_code(id) is not None:
            regions_with_data = get_regions_with_data(id)
            regions = get_regions_of_region(1)
            regions_without_data = filter(lambda region: region not in regions_with_data, regions)
            if len(regions_without_data) == len(regions):
                regions_without_data.append(region_service.get_by_code(1))
            translate_region_list(regions_without_data)
        else:
            abort(404)
        return response_xml_or_json_list(request, regions_without_data, 'regions', 'region')


class IndicatorByCountryAndPeriodAPI(Resource):
    """
    Countries element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, indicator_id, iso3):
        """
        Show observations by its indicator id and countyr id
        Observations will be filtered between two dates, if they are not supplied
        whole range will be returned
        Response 200 OK
        """
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        from_date, to_date = str_date_to_date(date_from, date_to)
        if country_service.get_by_code(iso3) is not None and indicator_service.get_by_code(indicator_id):
            country = country_service.get_by_code(iso3)
            observations = observation_service.get_all()
            observations = [obs for obs in observations if obs.region_id == country.id]
            observations = [obs for obs in observations if obs.indicator_id == indicator_id]
            observations = filter_observations_by_date_range(observations, from_date, to_date)
        else:
            abort(404)
        return response_xml_or_json_list(request, observations, 'observations', 'observation')


class IndicatorAverageByPeriodAPI(Resource):
    """
    Average of indicator observation by period range
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show average of indicator observations
        Observations will be filtered between two dates, if they are not supplied
        whole range will be returned
        Response 200 OK
        """
        date_from = request.args.get("from")
        date_to = request.args.get("to")
        from_date, to_date = str_date_to_date(date_from, date_to)
        observations = observation_service.get_all()
        observations = [obs for obs in observations if obs.indicator_id == id]
        observations = filter_observations_by_date_range(observations, from_date, to_date)
        if len(observations) > 0:
            average = observations_average(observations)
            element = EmptyObject()
            element.value = average
        else:
            abort(404)
        return response_xml_or_json_item(request, element, 'average')


class IndicatorRelatedAPI(Resource):
    """
    Indicator related collection URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, id):
        """
        Show related indicators
        Response 200 OK
        """
        indicators_relation = indicator_relationship_service.get_all()
        indicators_by_id = [indicator for indicator in indicators_relation if indicator.source_id == id]
        indicators_related = [indicator.target for indicator in indicators_by_id]
        translate_indicator_list(indicators_related)
        return response_xml_or_json_list(request, indicators_related, "indicators", "indicator")


class IndicatorCountryTendencyAPI(Resource):
    """
    Indicator country tendency element URI
    Methods: GET
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, indicator_id, iso3):
        """
        Show indicator tendency for a country and indicator
        Response 200 OK
        """
        indicator = (observation.indicator for observation in country_service.get_by_code(iso3).observations
                      if observation.indicator.id == indicator_id).next()
        response_object = EmptyObject()
        response_object.indicator_id = indicator.id
        response_object.iso3 = iso3
        response_object.tendency = indicator.preferable_tendency
        return response_xml_or_json_item(request, response_object, "tendency")


class RegionTranslationListAPI(Resource):
    """
    Region translation collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all translations of a region
        Response 200 OK
        """
        return response_xml_or_json_list(request, region_translation_service.get_all(), 'translations', 'translation')

    @localhost_decorator
    def post(self):
        """
        Create a new region translation
        Response 201 CREATED
        :return: URI
        """
        translation = RegionTranslation(request.json.get("lang_code"), request.json.get("name"),
                                        request.json.get("region_id"))
        if translation.lang_code is not None and translation.region_id is not None:
            region_translation_service.insert(translation)
            return {'URI': url_for('region_translations', lang_code=translation.lang_code, region_id=translation.region_id)}, 201 #returns the URI for the new country
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all region translation
        Response 204 NO CONTENT
        """
        translation_list = json.loads(request.data)
        translation_list = list_converter.convert(translation_list)
        region_translation_service.update_all(translation_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all region translations
        Response 204 NO CONTENT
        :attention: Take care of what you do, all regions translations will be destroyed
        """
        region_translation_service.delete_all()
        return {}, 204


class RegionTranslationAPI(Resource):
    """
    Region translation element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, region_id, lang_code):
        """
        Show region translation
        Response 200 OK
        """
        translation = region_translation_service.get_by_codes(region_id, lang_code)
        if translation is None:
            abort(404)
        return response_xml_or_json_item(request, translation, 'translation')

    @localhost_decorator
    def put(self, region_id, lang_code):
        """
        If exists update region translation
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        translation = region_translation_service.get_by_codes(region_id, lang_code)
        if translation is not None:
            translation.name = request.json.get("name")
            region_translation_service.update(translation)
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, region_id, lang_code):
        """
        Delete region translation
        Response 204 NO CONTENT
        """
        region_translation_service.delete(region_id, lang_code)
        return {}, 204


class IndicatorTranslationListAPI(Resource):
    """
    Indicators translations collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all indicators translations
        Response 200 OK
        """
        return response_xml_or_json_list(request, indicator_translation_service.get_all(), 'translations', 'translation')

    @localhost_decorator
    def post(self):
        """
        Create a new indicator translation
        Response 201 CREATED
        :return: URI
        """
        translation = IndicatorTranslation(request.json.get("lang_code"), request.json.get("name"),
                                        request.json.get("description"), request.json.get("indicator_id"))
        if translation.lang_code is not None and translation.indicator_id is not None:
            indicator_translation_service.insert(translation)
            return {'URI': url_for('indicator_translations', lang_code=translation.lang_code, indicator_id=translation.indicator_id)}, 201 #returns the URI for the new country
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all indicators translations given
        Response 204 NO CONTENT
        """
        translation_list = json.loads(request.data)
        translation_list = list_converter.convert(translation_list)
        indicator_translation_service.update_all(translation_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all indicators translations
        Response 204 NO CONTENT
        :attention: Take care of what you do, all indicators translations will be destroyed
        """
        indicator_translation_service.delete_all()
        return {}, 204


class IndicatorTranslationAPI(Resource):
    """
    Indicators translations element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, indicator_id, lang_code):
        """
        Show indicator translation
        Response 200 OK
        """
        translation = indicator_translation_service.get_by_codes(indicator_id, lang_code)
        if translation is None:
            abort(404)
        return response_xml_or_json_item(request, translation, 'translation')

    @localhost_decorator
    def put(self, indicator_id, lang_code):
        """
        If exists update indicator translation
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        translation = indicator_translation_service.get_by_codes(indicator_id, lang_code)
        if translation is not None:
            translation.name = request.json.get("name")
            translation.description = request.json.get("description")
            indicator_translation_service.update(translation)
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, indicator_id, lang_code):
        """
        Delete indicator translation
        Response 204 NO CONTENT
        """
        indicator_translation_service.delete(indicator_id, lang_code)
        return {}, 204


class TopicTranslationListAPI(Resource):
    """
    Topic translations collection URI
    Methods: GET, POST, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self):
        """
        List all topic translations
        Response 200 OK
        """
        return response_xml_or_json_list(request, topic_translation_service.get_all(), 'translations', 'translation')

    @localhost_decorator
    def post(self):
        """
        Create a new topic translation
        Response 201 CREATED
        :return: URI
        """
        translation = TopicTranslation(request.json.get("lang_code"), request.json.get("name"),
                                        request.json.get("topic_id"))
        if translation.lang_code is not None and translation.topic_id is not None:
            topic_translation_service.insert(translation)
            return {'URI': url_for('topic_translations', lang_code=translation.lang_code, topic_id=translation.topic_id)}, 201 #returns the URI for the new country
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self):
        """
        Update all topic translations given
        Response 204 NO CONTENT
        """
        translation_list = json.loads(request.data)
        translation_list = list_converter.convert(translation_list)
        topic_translation_service.update_all(translation_list)
        return {}, 204

    @localhost_decorator
    def delete(self):
        """
        Delete all topic translations
        Response 204 NO CONTENT
        :attention: Take care of what you do, all topic translations will be destroyed
        """
        topic_translation_service.delete_all()
        return {}, 204


class TopicTranslationAPI(Resource):
    """
    Topic translations element URI
    Methods: GET, PUT, DELETE
    """

    @requires_auth
    @cache.cached(key_prefix=make_cache_key)
    def get(self, topic_id, lang_code):
        """
        Show country topic translation
        Response 200 OK
        """
        translation = topic_translation_service.get_by_codes(topic_id, lang_code)
        if translation is None:
            abort(404)
        return response_xml_or_json_item(request, translation, 'translation')

    @localhost_decorator
    def put(self, topic_id, lang_code):
        """
        If exists update topic translation
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        translation = topic_translation_service.get_by_codes(topic_id, lang_code)
        if translation is not None:
            translation.name = request.json.get("name")
            topic_translation_service.update(translation)
            return {}, 204
        else:
            abort(400)

    @localhost_decorator
    def delete(self, topic_id, lang_code):
        """
        Delete topic translation
        Response 204 NO CONTENT
        """
        topic_translation_service.delete(topic_id, lang_code)
        return {}, 204


class DeleteCacheAPI(Resource):
    """
    Delete cache URI
    Methods: DELETE
    """

    @localhost_decorator
    def delete(self):
        """
        Delete cache
        Response 204 NO CONTENT
        """
        cache.clear()
        return {}, 204


@app.route('/graphs/barchart')
def barChart():
        """
        Visualization of barchart
        """
        options, title, description = get_visualization_json(request, 'bar')
        return response_graphics(options, title, description)


@app.route('/graphs/piechart')
def pieChart():
        """
        Visualization of piechart
        """
        options, title, description = get_visualization_json(request, 'pie')
        return response_graphics(options, title, description)


@app.route('/graphs/linechart')
def lineChart():
        """
        Visualization of linechart
        """
        options, title, description = get_visualization_json(request, 'line')
        return response_graphics(options, title, description)


@app.route('/graphs/areachart')
def areaChart():
        """
        Visualization of areachart
        """
        options, title, description = get_visualization_json(request, 'area')
        return response_graphics(options, title, description)


@app.route('/graphs/scatterchart')
def scatterChart():
        """
        Visualization of scatterchart
        """
        indicators = request.args.get('indicator').split(',')
        indicators = [indicator_service.get_by_code(indicator) for indicator in indicators]
        countries = request.args.get('countries')
        if countries == 'all':
            countries = country_service.get_all()
        else:
            countries = countries.split(',')
            countries = [country for country in country_service.get_all() if country.iso3 in countries]
        colours = request.args.get('colours').split(',')
        colours = ['#'+colour for colour in colours]
        title = request.args.get('title') if request.args.get('title') is not None else ''
        description = request.args.get('description') if request.args.get('description') is not None else ''
        xTag = request.args.get('xTag')
        yTag = request.args.get('yTag')
        from_time = datetime.strptime(request.args.get('from'), "%Y%m%d").date() if request.args.get('from') is not None else None
        to_time = datetime.strptime(request.args.get('to'), "%Y%m%d").date() if request.args.get('to') is not None else None
        series = []
        for country in countries:
            observations_x_indicator = filter_observations_by_date_range([observation for observation in country.observations \
                                                          if observation.indicator_id == indicators[1].id], from_time, to_time)
            observations_y_indicator = filter_observations_by_date_range([observation for observation in country.observations \
                                                          if observation.indicator_id == indicators[0].id], from_time, to_time)
            if len(observations_y_indicator) > 0 and len(observations_x_indicator) > 0:
                observations_x_indicator.sort(key=lambda observations: observation.ref_time.value)
                observations_y_indicator.sort(key=lambda observations: observation.ref_time.value)
                series.append({
                    'name': country.translations[0].name,
                    'values': [[float(observations_x_indicator[i].value.value) if observations_x_indicator[i].value.value is not None else 0,
                                float(observations_y_indicator[i].value.value) if observations_y_indicator[i].value.value is not None else 0]
                               for i in range(min(len(observations_x_indicator), len(observations_y_indicator)))]
                })
        json_object = {
            'chartType': 'scatter',
            'xAxis': {
                'title': xTag
            },
            'yAxis': {
                'title': yTag
            },
            'series': series,
            'serieColours': colours,
            'valueOnItem': {
                'show': False
            }
        }
        return response_graphics(json_object, title, description)


@app.route('/graphs/polarchart')
def polarChart():
        """
        Visualization of polarchart
        """
        options, title, description = get_visualization_json(request, 'polar')
        return response_graphics(options, title, description)


@app.route('/graphs/table')
def table():
        """
        Visualization of table
        """
        options, title, description = get_visualization_json(request, 'table')
        return response_graphics(options, title, description)


@app.route('/')
def help():
    """
    Main URI with the documentation redirection
    """
    return redirect('http://weso.github.io/landportal-data-access-api/', code=302)


class AuthAPI(Resource):
    """
    Auth URI
    Methods: POST, PUT
    """

    @localhost_decorator
    def post(self):
        """
        Create a new auth user
        Response 201 CREATED
        """
        auth = Auth(request.json.get('user'), request.json.get('token'))
        if auth.user is not None and auth.token is not None:
            auth_service.insert(auth)
            return 201
        abort(400)  # in case something is wrong

    @localhost_decorator
    def put(self, username):
        """
        If exists update auth user
        Response 204 NO CONTENT
        If not
        Response 400 BAD REQUEST
        """
        auth = auth_service.get_by_code(username)
        if auth is not None:
            auth.token = request.json.get("token")
            auth_service.update(auth)
            return {}, 204
        else:
            abort(400)


api.add_resource(CountryListAPI, '/countries', endpoint='countries_list')
api.add_resource(CountryAPI, '/countries/<code>', endpoint='countries')
api.add_resource(IndicatorListAPI, '/indicators', endpoint='indicators_list')
api.add_resource(IndicatorAPI, '/indicators/<id>', endpoint='indicators')
api.add_resource(IndicatorTopAPI, '/indicators/<id>/top', endpoint='indicators_top')
api.add_resource(IndicatorAverageAPI, '/indicators/<id>/average', endpoint='indicators_average')
api.add_resource(IndicatorCompatibleAPI, '/indicators/<id>/compatible', endpoint='indicators_compatible')
api.add_resource(UserListAPI, '/users', endpoint='users_list')
api.add_resource(UserAPI, '/users/<id>', endpoint='users')
api.add_resource(OrganizationListAPI, '/organizations', endpoint='organizations_list')
api.add_resource(OrganizationAPI, '/organizations/<id>', endpoint='organizations')
api.add_resource(OrganizationUserListAPI, '/organizations/<organization_id>/users', endpoint='organizations_users_list')
api.add_resource(OrganizationUserAPI, '/organizations/<organization_id>/users/<user_id>', endpoint='organizations_users')
api.add_resource(CountriesIndicatorListAPI, '/countries/<iso3>/indicators', endpoint='countries_indicators_list')
api.add_resource(CountriesIndicatorAPI, '/countries/<iso3>/indicators/<indicator_id>', endpoint='countries_indicators')
api.add_resource(ObservationListAPI, '/observations', endpoint='observations_list')
api.add_resource(ObservationAPI, '/observations/<id>', endpoint='observations')
api.add_resource(ObservationByTwoAPI, '/observations/<id_first_filter>/<id_second_filter>', endpoint='observations_by_two')
api.add_resource(ObservationByCountryStarred, '/observations/<iso3>/starred', endpoint='observations_by_country_starred')
api.add_resource(ObservationByTwoAverageAPI, '/observations/<id_first_filter>/<id_second_filter>/average', endpoint='observations_by_two_average')
api.add_resource(RegionListAPI, '/regions', endpoint='regions_list')
api.add_resource(RegionAPI, '/regions/<id>', endpoint='regions')
api.add_resource(RegionsCountryListAPI, '/regions/<id>/countries', endpoint='regions_countries_list')
api.add_resource(RegionsCountryAPI, '/regions/<id>/countries/<iso3>', endpoint='regions_countries')
api.add_resource(RegionsRegionListAPI, '/regions/<id>/regions', endpoint='regions_regions_list')
api.add_resource(DataSourceListAPI, '/datasources', endpoint='datasources_list')
api.add_resource(DataSourceAPI, '/datasources/<id>', endpoint='datasources')
api.add_resource(DatasetListAPI, '/datasets', endpoint='datasets_list')
api.add_resource(DatasetAPI, '/datasets/<id>', endpoint='datasets')
api.add_resource(DataSourceIndicatorListAPI, '/datasources/<id>/indicators', endpoint='datasources_indicators_list')
api.add_resource(DataSourceIndicatorAPI, '/datasources/<id>/indicators/<indicator_id>', endpoint='datasources_indicators')
api.add_resource(ValueListAPI, '/values', endpoint='value_list')
api.add_resource(ValueAPI, '/values/<id>', endpoint='values')
api.add_resource(TopicListAPI, '/topics', endpoint='topic_list')
api.add_resource(TopicAPI, '/topics/<id>', endpoint='topics')
api.add_resource(TopicIndicatorListAPI, '/topics/<topic_id>/indicators', endpoint='topics_indicators_list')
api.add_resource(TopicIndicatorAPI, '/topics/<topic_id>/indicators/<indicator_id>', endpoint='topics_indicators')
api.add_resource(MeasurementUnitListAPI, '/measurement_units', endpoint='measurement_units_list')
api.add_resource(MeasurementUnitAPI, '/measurement_units/<id>', endpoint='measurement_unit')
api.add_resource(RegionCountriesWithDataAPI, '/regions/<region_id>/countries_with_data', endpoint='regions_countries_with_data')
api.add_resource(CountriesIndicatorLastUpdateAPI, '/countries/<iso3>/last_update', endpoint='countries_indicators_last_update')
api.add_resource(IndicatorsCountryLastUpdateAPI, '/indicators/<id>/<iso3>/last_update', endpoint='indicators_countries_last_update')
api.add_resource(ObservationByPeriodAPI, '/observations/<id>/range', endpoint='observations_by_period')
api.add_resource(IndicatorByPeriodAPI, '/indicators/<id>/range', endpoint='indicators_by_period')
api.add_resource(IndicatorRegionsWithDataAPI, '/indicators/<id>/regions_with_data', endpoint='indicators_regions_with_data')
api.add_resource(IndicatorRegionsWihtoutDataAPI, '/indicators/<id>/regions_without_data', endpoint='indicators_regions_without_data')
api.add_resource(IndicatorAverageByPeriodAPI, '/indicators/<id>/average/range', endpoint='indicators_average_by_period')
api.add_resource(IndicatorByCountryAndPeriodAPI, '/indicators/<indicator_id>/<iso3>/range', endpoint='indicators_by_country_and_period')
api.add_resource(IndicatorRelatedAPI, '/indicators/<id>/related', endpoint='indicators_related')
api.add_resource(IndicatorCountryTendencyAPI, '/indicators/<indicator_id>/<iso3>/tendency', endpoint='indicator_country_tendency')
api.add_resource(RegionTranslationListAPI, '/regions/translations', endpoint='region_translation_list')
api.add_resource(RegionTranslationAPI, '/regions/translations/<region_id>/<lang_code>', endpoint='region_translations')
api.add_resource(IndicatorTranslationListAPI, '/indicators/translations', endpoint='indicator_translation_list')
api.add_resource(IndicatorTranslationAPI, '/indicators/translations/<indicator_id>/<lang_code>', endpoint='indicator_translations')
api.add_resource(TopicTranslationListAPI, '/topics/translations', endpoint='topic_translation_list')
api.add_resource(TopicTranslationAPI, '/topics/translations/<topic_id>/<lang_code>', endpoint='topic_translations')
api.add_resource(IndicatorStarredAPI, '/indicators/starred', endpoint='indicator_starred')
api.add_resource(DeleteCacheAPI, '/cache', endpoint='delete_cache')
api.add_resource(AuthAPI, '/auth', endpoint='auth')


def translate_indicator_list(indicators):
    """
    Translate an indicator list into given language
    :param indicators: list of indicators to be translated
    """
    lang = get_requested_lang()
    for indicator in indicators:
        translate_indicator(indicator, lang)


def translate_indicator(indicator, lang=None):
    """
    Translate an indicator object into given language
    :param indicator: indicator object to be translated
    :param lang: language of translation, by default en
    """
    if lang is None:
        lang = get_requested_lang()
    translation = indicator_translation_service.get_by_codes(indicator.id, lang)
    if translation is not None:
        indicator.name = translation.name
        indicator.description = translation.description
        indicator.other_parseable_fields = ['name', 'description']


def translate_region_list(regions):
    """
    Translate a region list into given language
    :param regions: list of regions to be translated
    """
    lang = get_requested_lang()
    for region in regions:
        translate_region(region, lang)


def translate_region(region, lang=None):
    """
    Translate a region object into given language
    :param region: region object to be translated
    :param lang: language of translation, by default en
    """
    if lang is None:
        lang = get_requested_lang()
    translation = region_translation_service.get_by_codes(region.id, lang)
    if translation is not None:
        region.name = translation.name
        region.other_parseable_fields = ['name']


def translate_topic_list(topics):
    """
    Translate a topic list into given language
    :param topics: list of topics to be translated
    """
    lang = get_requested_lang()
    for topic in topics:
        translate_topic(topic, lang)


def translate_topic(topic, lang=None):
    """
    Translate a topic object into given language
    :param topic: topic object to be translated
    :param lang: language of translation, by default en
    """
    if lang is None:
        lang = get_requested_lang()
    translation = topic_translation_service.get_by_codes(topic.id, lang)
    if translation is not None:
        topic.translation_name = translation.name
        topic.other_parseable_fields = ['translation_name']


def get_requested_lang():
    """
    Returns the lang request
    :return: language requested by the client if not given *en* as default
    """
    lang = request.args.get('lang') if request.args.get('lang') is not None else 'en'
    return lang


def is_xml_accepted(request):
    """
    Returns if xml is accepted or not
    :return: True if xml is accepted, False otherwise
    """
    return request.args.get('format') == "xml"


def is_jsonp_accepted(request):
    """
    Returns if jsonp is accepted or not
    :return: True if jsonp is accepted, False otherwise
    """
    return request.args.get('format') == "jsonp"


def is_csv_accepted(request):
    """
    Returns if csv is accepted or not
    :return: True if csv is accepted, False otherwise
    """
    return request.args.get('format') == "csv"


def response_xml_or_json_item(request, item, item_string):
    """
    Return response with the content in the format requested
    Available formats:
    * JSON
    * XML
    * JSONP
    * CSV
    :param request: the request object
    :param item: the object to be converted
    :param item_string: the string text to show in the root node, only needed for xml
    :return: response in the requested format
    """
    if is_xml_accepted(request):
        return Response(xml_converter.object_to_xml(item,
                                                    item_string), mimetype='application/xml')
    elif is_jsonp_accepted(request):
        function = request.args.get('jsonp') if request.args.get('jsonp') is not None else 'callback'
        response = function + '(' + json_converter.object_to_json(item) + ');'
        return Response(response, mimetype='application/javascript')
    elif is_csv_accepted(request):
        response = Response(csv_converter.object_to_csv(item
                                                    ), mimetype='text/csv', content_type='application/octet-stream')
        response.headers["Content-Disposition"] = 'attachment; filename=' + item_string + '.csv'
        return response
    else:
        return Response(json_converter.object_to_json(item
                                                      ), mimetype='application/json')


def response_xml_or_json_list(request, collection, collection_string, item_string):
    """
    Return response with the content in the format requested
    Available formats:
    * JSON
    * XML
    * JSONP
    * CSV
    :param request: the request object
    :param collection: the collection to be converted
    :param collection_string: the string text to show in the root node, only needed for xml
    :param item_string: the string in the root node of the object, only needed for xml
    :return: response in the requested format
    """
    if is_xml_accepted(request):
        return Response(xml_converter.list_to_xml(collection,
                                                  collection_string, item_string), mimetype='application/xml')
    elif is_jsonp_accepted(request):
        function = request.args.get('jsonp') if request.args.get('jsonp') is not None else 'callback'
        response = function + '(' + json_converter.list_to_json(collection) + ');'
        return Response(response, mimetype='application/javascript')
    elif is_csv_accepted(request):
        response = Response(csv_converter.list_to_csv(collection
                                ), mimetype='text/csv', content_type='application/octet-stream')
        response.headers["Content-Disposition"] = 'attachment; filename="' + collection_string + '".csv'
        return response
    else:
        return Response(json_converter.list_to_json(collection
                                                    ), mimetype='application/json')


def filter_observations_by_date_range(observations, from_date=None, to_date=None):
    """
    Filters observations by a given date range
    :param observations: list of observations to filter
    :param from_date: beginning of the date range
    :param to_date: end of the date range
    :return: filtered list of observations
    """
    def filter_key(observation):
        """
        Filters a single observations
        :param observation: observations to filter
        :return: True if observations passes, False otherwise
        """
        time = observation.ref_time
        return (isinstance(time, Instant) and from_date <= time.timestamp <= to_date) \
            or (isinstance(time, Interval) and time.start_time <= to_date and time.end_time >= from_date)  \
            or (isinstance(time, YearInterval) and to_date.year <= time.year <= from_date.year)

    return filter(filter_key, observations) if from_date is not None and to_date is not None else observations


def str_date_to_date(date_from, date_to):
    """
    Convert two dates in str format to date object
    Format: YYYYMMDD
    :param date_from: beginning of the interval
    :param date_to: end of the interval
    :return: from_date and to_date equivalent of given in date objects
    """
    if date_from is not None and date_to is not None:
        from_date = datetime.strptime(date_from, "%Y%m%d").date()
        to_date = datetime.strptime(date_to, "%Y%m%d").date()
    return from_date, to_date


def filter_by_region_and_top(id):
    """
    Filter by region and a top given
    :return: countries top and top observations
    """
    top = int(request.args.get("top")) if request.args.get("top") is not None else 10
    region = int(request.args.get("region")) if request.args.get("region") not in (None, "global") else "global"
    if region is 'global':
        observations = observation_service.get_all()
        observations = [obs for obs in observations if obs.indicator_id == id]
        observations = sorted(observations, key=lambda obs: float(obs.value.value)
                              if obs.value.value is not None else 0, reverse=True)
    else:
        countries = country_service.get_all()
        countries = [country for country in countries if country.is_part_of_id == region]
        observations = []
        for country in countries:
            observations.extend(country.observations)
    countries = country_service.get_all()  # improve if changing directionality of model on observation country
    top = observations[:top]
    countries = [country for observation in top for country in countries if observation.region_id == country.id]
    return countries, top


def observations_average(observations):
    """
    Returns the average of observations values
    :param observations: observations to calculate the average
    :return: average
    """
    observations = [observation for observation in observations if observation.value.value is not None]
    if len(observations) == 1:
        average = observations[0].value.value
    elif len(observations) == 0:
        return 0
    else:
        average = 0
        for observation in observations:
            average += float(observation.value.value)
    return float(average)/len(observations)


def get_visualization_json(request, chartType):
    """
    Create json object through a dict by request parameters given
    :param request: request object from the client
    :param chartType: type of chart to be showed
    :return: json_object, dict to make json.dumps; title, title of the graphic; description, descriptions of the graphic
    """
    indicator = indicator_service.get_by_code(request.args.get('indicator'))
    countries = request.args.get('countries').split(',')
    countries = [country for country in country_service.get_all() if country.iso3 in countries]
    colours = request.args.get('colours').split(',')
    colours = ['#'+colour for colour in colours]
    title = request.args.get('title') if request.args.get('title') is not None else ''
    description = request.args.get('description') if request.args.get('description') is not None else ''
    xTag = request.args.get('xTag')
    yTag = request.args.get('yTag')
    from_time = datetime.strptime(request.args.get('from'), "%Y%m%d").date() if request.args.get('from') is not None else None
    to_time = datetime.strptime(request.args.get('to'), "%Y%m%d").date() if request.args.get('to') is not None else None
    series = []
    for country in countries:
        observations = filter_observations_by_date_range([observation for observation in country.observations \
                                                      if observation.indicator_id == indicator.id], from_time, to_time)
        if len(observations) > 10:  # limit to ten, to ensure good view
            observations = observations[-10:]
        times = [observation.ref_time for observation in observations]
        series.append({
            'name': country.translations[0].name,
            'values': [float(observation.value.value) if observation.value.value is not None
                       else None for observation in observations]
        })
    json_object = {
        'chartType': chartType,
        'xAxis': {
            'title': xTag,
            'values': get_intervals(times)
        },
        'yAxis': {
            'title': yTag
        },
        'series': series,
        'serieColours': colours,
        'valueOnItem': {
            'show': False
        }
    }
    return json_object, title, description


def get_intervals(times):
    """
    Return intervals to xAxis on the graphic
    :param times: times collection
    :return: times in the format of the graphic
    """
    # if len(times) > 1:
    #     if isinstance(times[0], Instant):
    #         return [time.timestamp for time in times]
    #     elif isinstance(times[0], YearInterval):
    #         return [time.year for time in times]
    #     elif isinstance(times[0], Interval):
    #         return [time.start_time for time in times]
    # elif len(times) == 1:
    #     if isinstance(times[0], Instant):
    #         return [times[0].timestamp]
    #     elif isinstance(times[0], YearInterval):
    #         return [times[0].year]
    #     elif isinstance(times[0], Interval):
    #         return [times[0].start_time]
    return [time.value for time in times]


def response_graphics(options, title, description):
    """
    Reponses with a page containing the requested graphic
    :param options: options dict
    :param title: title for the graphic
    :param description: description for the graphic
    """
    if request.args.get("format") == "json":
        return Response(json.dumps(options), mimetype='application/json')
    elif request.args.get("format") == 'jsonp':
        return Response("callback("+json.dumps(options)+");", mimetype='application/javascript')
    return render_template('graphic.html', options=json.dumps(options), title=title, description=description)


def get_regions_of_region(id):
    """
    Returns the regions that belong to another region
    :param id: id of the region
    :return: list of regions
    """
    region = region_service.get_by_code(id)
    regions = []
    for selectedRegion in region_service.get_all():
        if selectedRegion.is_part_of_id == region.id:
            regions.append(selectedRegion)
    translate_region_list(regions)
    return regions


def get_regions_with_data(id):
    """
    Return all the regions with data for a given indicator
    :param id: id of the given indicator
    :return: list of regions with data
    """
    regions_with_data = []
    regions = get_regions_of_region(1)
    observations = observation_service.get_all()
    observations = [obs for obs in observations if obs.indicator_id == id]
    regions_observations_id = [obs.region_id for obs in observations]
    for region in regions:
        ids_countries = [country.id for country in country_service.get_all() if country.is_part_of_id == region.id]
        for id in ids_countries:
            if id in regions_observations_id:
                try:
                    regions_with_data.index(region)
                except ValueError:
                    regions_with_data.append(region)
    if len(regions_with_data) > 0:
        regions_with_data.append(region_service.get_by_code(1))
    translate_region_list(regions_with_data)
    return regions_with_data


class EmptyObject():
    """
    Class to create object without attributes, to be included dynamically
    """
    def __init__(self):
        pass

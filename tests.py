
__author__ = 'Herminio'

import unittest
import app
import json
from flask_testing import TestCase
from app.utils import JSONConverter
from time import time
from datetime import datetime
from model import models

json_converter = JSONConverter()


class MyProxyHack(object):
    """
    Hack to proxy in testing, if not will fail because of bad ip address
    @see http://stackoverflow.com/questions/14872829/get-ip-address-when-testing-flask-application-through-nosetests
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['REMOTE_ADDR'] = environ.get('REMOTE_ADDR', '127.0.0.1')
        return self.app(environ, start_response)


class ApiTest(TestCase):
    """
    Generic class for all test concerning Flask on this API
    """
    def create_app(self):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
        app.app.config['TESTING'] = True
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
        app.app.wsgi_app = MyProxyHack(app.app.wsgi_app)
        return app.app

    def setUp(self):
        app.db.drop_all()
        app.db.create_all()

    def tearDown(self):
        app.db.session.remove()
        app.db.drop_all()


class TestCountry(ApiTest):
    def test_item(self):
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        spain_updated = json.dumps(dict(
            iso2='SP',
            iso3='ESP'
        ))
        response = self.client.get("/countries/ESP")
        self.assert404(response)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/countries/ESP")
        self.assertEquals(response.json.get('iso2'), "ES")
        self.assertEquals(response.json.get('iso3'), "ESP")
        response = self.client.put("/countries/ESP", data=spain_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/countries/ESP")
        self.assertEquals(response.json.get('iso2'), "SP")
        response = self.client.delete("/countries/ESP")
        self.assertStatus(response, 204)
        response = self.client.get("/countries/ESP")
        self.assert404(response)

    def test_collection(self):
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        france_json = json.dumps(dict(
            name='France',
            iso2='FR',
            iso3='FRA'
        ))
        countries_updated = json.dumps([
            dict(iso2='SP', iso3='ESP'),
            dict(iso2='FR', iso3='FRA')
        ])
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=france_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/countries")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['iso2'], "ES")
        self.assertEquals(spain['iso3'], "ESP")
        self.assertEquals(france['iso2'], "FR")
        self.assertEquals(france['iso3'], "FRA")
        response = self.client.put("/countries", data=countries_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/countries")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['iso2'], "SP")
        self.assertEquals(france['iso2'], "FR")
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_indicator_subcolecction_item(self):
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           id=1
        ))
        indicator_json = json.dumps(dict(
           id=1,
           name='donation',
           description='A gives a donation to B'
        ))
        observation_json = json.dumps(dict(
           id=1,
           id_source=1,
           indicator_id=1,
           region_id=1
        ))
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/countries/ESP/indicators/1")
        self.assert404(response)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/countries/ESP/indicators/1")
        self.assertEquals(response.json.get('id'), "1")
        response = self.client.delete("/countries/ESP")
        self.assertStatus(response, 204)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/countries/ESP")
        self.assert404(response)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

    def test_indicator_subcolecction_collection(self):
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        indicator_json = json.dumps(dict(
           id=1,
           name='donation',
           description='A gives a donation to B'
        ))
        indicator2_json = json.dumps(dict(
           id=2,
           name='donation',
           description='B gives a donation to A'
        ))
        observation_json = json.dumps(dict(
           id=1,
           id_source=1,
           indicator_id=1,
           region_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           id_source=2,
           indicator_id=2,
           region_id=1
        ))
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/countries/ESP/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/countries/ESP/indicators")
        indicator = response.json[0]
        indicator2 = response.json[1]
        self.assertEquals(indicator['id'], "1")
        self.assertEquals(indicator2['id'], "2")
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/countries")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)


class TestIndicator(ApiTest):
    def test_item(self):
        indicator_json = json.dumps(dict(
            id=1,
            name='donation',
            description='donation from A to B'
        ))
        indicator_updated = json.dumps(dict(
            id=1,
            name='donation',
            description='donation from B to A'
        ))
        response = self.client.get("/indicators/1")
        self.assert404(response)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/1")
        self.assertEquals(response.json.get('id'), "1")
        response = self.client.put("/indicators/1", data=indicator_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/indicators/1")
        self.assertEquals(response.json.get('id'), "1")
        response = self.client.delete("/indicators/1")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators/1")
        self.assert404(response)

    def test_collection(self):
        donation_json = json.dumps(dict(
            id=1,
            name='donation',
            description='donation from A to B'
        ))
        receiver_json = json.dumps(dict(
            id=2,
            name='receiver',
            description='receives a donation from B'
        ))
        indicators_updated = json.dumps([
            dict(id=1, name='donation', description='donation from B to A'),
            dict(id=2, name='receiver', description='receives a donation from A')
        ])
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=donation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=receiver_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/indicators")
        donation = response.json[0]
        receiver = response.json[1]
        self.assertEquals(donation['id'], "1")
        self.assertEquals(receiver['id'], "2")
        response = self.client.put("/indicators", data=indicators_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/indicators")
        self.assertEquals(len(response.json), 2)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)

    def test_indicator_top(self):
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           is_part_of_id=3,
           id=1
        ))
        france_json = json.dumps(dict(
            name='France',
            iso2='FR',
            iso3='FRA',
            is_part_of_id=3,
            id=2
        ))
        observation1_json = json.dumps(dict(
           id=1,
           id_source='1',
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           id_source='1',
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=2,
           indicator_id=1,
           dataset_id=1,
           region_id=2,
           slice_id=1
        ))
        value1_json = json.dumps(dict(
            id=1,
            value=50
        ))
        value2_json = json.dumps(dict(
            id=2,
            value=100
        ))
        indicator_json = json.dumps(dict(
            id=1,
            name='donation',
            description='A gives a donation to B',
            dataset_id=1
        ))
        region_json = json.dumps(dict(
            id=3,
            un_code='200',
            name='Europe'
        ))
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=france_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/values", data=value1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/values", data=value2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/1/top?region=global&top=10")
        france = response.json[0]
        spain = response.json[1]
        self.assertEquals(spain['iso3'], "ESP")
        self.assertEquals(spain['value_id'], "1")
        self.assertEquals(france['value_id'], "2")
        self.assertEquals(france['iso3'], "FRA")
        response = self.client.get("/indicators/1/top?region=3&top=1")
        self.assertEquals(len(response.json), 1)
        spain = response.json[0]
        self.assertEquals(spain['iso3'], "ESP")
        self.assertEquals(spain['value_id'], "1")
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_indicator_average(self):
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           is_part_of_id=3,
           id=1
        ))
        france_json = json.dumps(dict(
            name='France',
            iso2='FR',
            iso3='FRA',
            is_part_of_id=3,
            id=2
        ))
        region_json = json.dumps(dict(
            id=3,
            un_code=200,
            name='Europe'
        ))
        observation1_json = json.dumps(dict(
           id=1,
           id_source='1',
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           id_source='1',
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=2,
           indicator_id=1,
           dataset_id=1,
           region_id=2,
           slice_id=1
        ))
        value1_json = json.dumps(dict(
            id=1,
            value=50
        ))
        value2_json = json.dumps(dict(
            id=2,
            value=100
        ))
        indicator_json = json.dumps(dict(
            id=1,
            name='donation',
            description='A gives a donation to B',
            dataset_id=1
        ))
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=france_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/values", data=value1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/values", data=value2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/1/average?region=global&top=10")
        self.assertEquals(response.json['value'], 75)
        response = self.client.get("/indicators/1/average?region=3&top=1")
        self.assertEquals(response.json['value'], 50)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_indicator_compatible(self):
        indicator1_json = json.dumps(dict(
            id=1,
            name="One",
            measurement_unit_id=1
        ))
        indicator2_json = json.dumps(dict(
            id=2,
            name="Two",
            measurement_unit_id=1
        ))
        indicator3_json = json.dumps(dict(
            id=3,
            name="Three",
            measurement_unit_id=2
        ))
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=indicator1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator3_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/1/compatible")
        self.assertEquals(len(response.json), 1)
        indicator = response.json[0]
        self.assertEquals(indicator['id'], "2")
        response = self.client.get("/indicators/3/compatible")
        self.assertEquals(len(response.json), 0)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)

    def test_starred(self):
        donation_json = json.dumps(dict(
            id=1,
            starred=False
        ))
        receiver_json = json.dumps(dict(
            id=2,
            starred=True
        ))
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=donation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=receiver_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/starred")
        self.assertEquals(len(response.json), 1)
        receiver = response.json[0]
        self.assertEquals(receiver['id'], "2")
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)


class TestUser(ApiTest):
    def test_item(self):
        user_json = json.dumps(dict(
           id='1',
           ip='192.168.1.1'
        ))
        user_updated = json.dumps(dict(
           id='1',
           ip='192.168.1.2'
        ))
        response = self.client.get("/users/1")
        self.assert404(response)
        response = self.client.post("/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/users/1")
        self.assertEquals(response.json.get('id'), "1")
        self.assertEquals(response.json.get('ip'), "192.168.1.1")
        response = self.client.put("/users/1", data=user_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/users/1")
        self.assertEquals(response.json.get('ip'), "192.168.1.2")
        response = self.client.delete("/users/1")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/users/1")
        self.assert404(response)

    def test_collection(self):
        user_json = json.dumps(dict(
           id='1',
           ip='192.168.1.1'
        ))
        user2_json = json.dumps(dict(
           id='2',
           ip='192.168.1.2',
        ))
        users_updated = json.dumps([
            dict(id='1', ip='192.168.1.3'),
            dict(id='2', ip='192.168.1.4')
        ])
        response = self.client.get("/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.post("/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/users", data=user2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/users")
        user = response.json[0]
        user2 = response.json[1]
        self.assertEquals(user['id'], "1")
        self.assertEquals(user['ip'], "192.168.1.1")
        self.assertEquals(user2['id'], "2")
        self.assertEquals(user2['ip'], "192.168.1.2")
        response = self.client.put("/users", data=users_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/users")
        user = response.json[0]
        user2 = response.json[1]
        self.assertEquals(user['ip'], "192.168.1.3")
        self.assertEquals(user2['ip'], "192.168.1.4")
        response = self.client.delete("/users")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)


class TestOrganization(ApiTest):
    def test_item(self):
        organization_json = json.dumps(dict(
           id='1',
           name='Organization A',
           url='http://www.organizationA.com'
        ))
        organization_updated = json.dumps(dict(
           id='1',
           name='Organization B',
           url='http://www.organizationB.com'
        ))
        response = self.client.get("/organizations/1")
        self.assert404(response)
        response = self.client.post("/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/organizations/1")
        self.assertEquals(response.json.get('id'), "1")
        self.assertEquals(response.json.get('name'), "Organization A")
        self.assertEquals(response.json.get('url'), "http://www.organizationA.com")
        response = self.client.put("/organizations/1", data=organization_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/organizations/1")
        self.assertEquals(response.json.get('name'), "Organization B")
        self.assertEquals(response.json.get('url'), "http://www.organizationB.com")
        response = self.client.delete("/organizations/1")
        self.assertStatus(response, 204)
        response = self.client.get("/organizations/1")
        self.assert404(response)

    def test_collection(self):
        organization_json = json.dumps(dict(
           id='1',
           name='Organization A',
           url='http://www.organizationA.com'
        ))
        organization2_json = json.dumps(dict(
           id='2',
           name='Organization B',
           url='http://www.organizationB.com'
        ))
        organizations_updated = json.dumps([
            dict(id='1', name='Organization C', url='http://www.organizationC.com'),
            dict(id='2', name='Organization D', url='http://www.organizationD.com')
        ])
        response = self.client.get("/organizations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)
        response = self.client.post("/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/organizations", data=organization2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/organizations")
        organization = response.json[0]
        organization2 = response.json[1]
        self.assertEquals(organization['id'], "1")
        self.assertEquals(organization['name'], "Organization A")
        self.assertEquals(organization['url'], "http://www.organizationA.com")
        self.assertEquals(organization2['id'], "2")
        self.assertEquals(organization2['name'], "Organization B")
        self.assertEquals(organization2['url'], "http://www.organizationB.com")
        response = self.client.put("/organizations", data=organizations_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/organizations")
        organization = response.json[0]
        organization2 = response.json[1]
        self.assertEquals(organization['name'], "Organization C")
        self.assertEquals(organization['url'], "http://www.organizationC.com")
        self.assertEquals(organization2['name'], "Organization D")
        self.assertEquals(organization2['url'], "http://www.organizationD.com")
        response = self.client.delete("/organizations")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/organizations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

    def test_user_subcolecction_item(self):
        organization_json = json.dumps(dict(
           id="1",
           name='Organization A',
           url='http://www.organizationA.com'
        ))
        user_json = json.dumps(dict(
           id="1",
           ip='192.168.1.1',
           organization_id="1"
        ))
        response = self.client.post("/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/organizations/1/users/1")
        self.assert404(response)
        response = self.client.post("/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/organizations/1/users/1")
        self.assertEquals(response.json.get('id'), "1")
        self.assertEquals(response.json.get('ip'), "192.168.1.1")
        response = self.client.delete("/organizations/1")
        self.assertStatus(response, 204)
        response = self.client.delete("/users")
        self.assertStatus(response, 204)
        response = self.client.get("/organizations/1")
        self.assert404(response)
        response = self.client.get("/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.delete("/organizations")
        self.assertStatus(response, 204)
        response = self.client.get("/organizations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

    def test_user_subcolecction_collection(self):
        organization_json = json.dumps(dict(
           id=1,
           name='Organization A',
           url='http://www.organizationA.com'
        ))
        user_json = json.dumps(dict(
           id=1,
           ip='192.168.1.1',
           organization_id=1
        ))
        user2_json = json.dumps(dict(
           id=2,
           ip='192.168.1.2',
           organization_id=1
        ))
        users_updated = json.dumps([
            dict(id='1', ip='192.168.1.3', organization_id=1),
            dict(id='2', ip='192.168.1.4', organization_id=1)
        ])
        response = self.client.post("/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/organizations/1/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.post("/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/users", data=user2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/organizations/1/users")
        user = response.json[0]
        user2 = response.json[1]
        self.assertEquals(user['id'], "1")
        self.assertEquals(user['ip'], "192.168.1.1")
        self.assertEquals(user2['id'], "2")
        self.assertEquals(user2['ip'], "192.168.1.2")
        response = self.client.delete("/users")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.delete("/organizations")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/organizations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)


class TestObservation(ApiTest):
    def test_item(self):
        observation_json = json.dumps(dict(
           id=1,
           dataset_id=1
        ))
        observation_updated = json.dumps(dict(
           id=1,
           dataset_id=2
        ))
        response = self.client.get("/observations/1")
        self.assert404(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/1")
        self.assertEquals(response.json.get('id'), "1")
        self.assertEquals(response.json.get('dataset_id'), 1)
        response = self.client.put("/observations/1", data=observation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/observations/1")
        self.assertEquals(response.json.get('id'), "1")
        self.assertEquals(response.json.get('dataset_id'), 2)
        response = self.client.delete("/observations/1")
        self.assertStatus(response, 204)
        response = self.client.get("/observations/1")
        self.assert404(response)

    def test_collection(self):
        observation_json = json.dumps(dict(
           id=1,
           dataset_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           dataset_id=2
        ))
        observation_updated = json.dumps([
            dict(id=1, id_source=2, dataset_id=2),
            dict(id=2, id_source=1, dataset_id=1)
        ])
        response = self.client.get("/observations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/observations")
        observation = response.json[0]
        observation2 = response.json[1]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation2['id'], "2")
        self.assertEquals(observation2['dataset_id'], 2)
        response = self.client.put("/observations", data=observation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/observations")
        observation = response.json[0]
        observation2 = response.json[1]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['dataset_id'], 2)
        self.assertEquals(observation2['id'], "2")
        self.assertEquals(observation2['dataset_id'], 1)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/observations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)


class TestRegion(ApiTest):
    def test_item(self):
        region_json = json.dumps(dict(
           id=1,
           name='Spain',
           un_code=200
        ))
        response = self.client.get("/regions/1")
        self.assert404(response)
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/200")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('un_code'), 200)
        response = self.client.delete("/regions/200")
        self.assertStatus(response, 204)
        response = self.client.get("/regions/200")
        self.assert404(response)

    def test_collection(self):
        region_json = json.dumps(dict(
           id='1',
           un_code=200
           #is_part_of_id=1
        ))
        region2_json = json.dumps(dict(
           id='2',
           un_code=201
           #is_part_of_id=2
        ))
        response = self.client.get("/regions")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions", data=region2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/regions")
        region = response.json[0]
        region2 = response.json[1]
        self.assertEquals(region['id'], 1)
        #self.assertEquals(region['is_part_of_id'], 1)
        self.assertEquals(region2['id'], 2)
        #self.assertEquals(region2['is_part_of_id'], 2)
        response = self.client.delete("/regions")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/regions")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

    def test_country_subcolecction_item(self):
        region_json = json.dumps(dict(
           id='1',
           un_code=200
           #is_part_of_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           is_part_of_id=1
        ))
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/200/countries/1")
        self.assert404(response)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/200/countries/ESP")
        self.assertEquals(response.json.get('iso2'), "ES")
        self.assertEquals(response.json.get('iso3'), "ESP")
        response = self.client.delete("/regions/200")
        self.assertStatus(response, 204)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/regions/200")
        self.assert404(response)
        response = self.client.get("/countries")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.delete("/regions")
        self.assertStatus(response, 204)
        response = self.client.get("/regions")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

    def test_country_subcolecction_collection(self):
        region_json = json.dumps(dict(
           id='1',
           name='Europe',
           un_code=200
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           is_part_of_id=1
        ))
        country2_json = json.dumps(dict(
           name='France',
           iso2='FR',
           iso3='FRA',
           is_part_of_id=1
        ))
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/1/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/200/countries")
        country = response.json[0]
        country2 = response.json[1]
        self.assertEquals(country['iso2'], "ES")
        self.assertEquals(country['iso3'], "ESP")
        self.assertEquals(country2['iso2'], "FR")
        self.assertEquals(country2['iso3'], "FRA")
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.delete("/regions")
        self.assertStatus(response, 204)
        response = self.client.get("/regions")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

    def test_country_with_data(self):
        region_json = json.dumps(dict(
           name='Europe',
           un_code=200,
           id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           id=2,
           is_part_of_id=1
        ))
        country2_json = json.dumps(dict(
           name='France',
           iso2='FR',
           iso3='FRA',
           id=3,
           is_part_of_id=1
        ))
        observation_json = json.dumps(dict(
            id='1',
            region_id=2
        ))
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/200/countries_with_data")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/200/countries_with_data")
        self.assertEquals(len(response.json), 1)
        country = response.json[0]
        self.assertEquals(country['iso2'], "ES")
        self.assertEquals(country['iso3'], "ESP")
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.delete("/regions")
        self.assertStatus(response, 204)
        response = self.client.get("/regions")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)


class TestDataSource(ApiTest):
    def test_item(self):
        datasource_json = json.dumps(dict(
           id=1,
           id_source='1',
           name='World Bank 1',
           organization_id=1
        ))
        datasource_updated = json.dumps(dict(
           id=1,
           id_source='1',
           name='World Bank 2',
           organization_id=1
        ))
        response = self.client.get("/datasources/1")
        self.assert404(response)
        response = self.client.post("/datasources", data=datasource_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/datasources/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('name'), "World Bank 1")
        self.assertEquals(response.json.get('organization_id'), "1")
        response = self.client.put("/datasources/1", data=datasource_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/datasources/1")
        self.assertEquals(response.json.get('name'), "World Bank 2")
        response = self.client.delete("/datasources/1")
        self.assertStatus(response, 204)
        response = self.client.get("/datasources/1")
        self.assert404(response)

    def test_collection(self):
        datasource_json = json.dumps(dict(
           id=1,
           id_source='1',
           organization_id=1
        ))
        datasource2_json = json.dumps(dict(
           id=2,
           id_source='1',
           name='World Bank 2',
           organization_id=1
        ))
        datasources_updated = json.dumps([
            dict(id=1, name='World Bank 3'),
            dict(id=2, name='World Bank 4')
        ])
        response = self.client.get("/datasources")
        self.assert200(response)
        datasources = response.json
        self.assertEquals(len(datasources), 0)
        response = self.client.post("/datasources", data=datasource_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/datasources", data=datasource2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/datasources")
        datasource = response.json[0]
        datasource2 = response.json[1]
        self.assertEquals(datasource['id'], 1)
        self.assertEquals(datasource['organization_id'], "1")
        self.assertEquals(datasource2['id'], 2)
        self.assertEquals(datasource2['organization_id'], "1")
        response = self.client.put("/datasources", data=datasources_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/datasources")
        datasource = response.json[0]
        datasource2 = response.json[1]
        response = self.client.delete("/datasources")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/datasources")
        self.assert200(response)
        datasources = response.json
        self.assertEquals(len(datasources), 0)

    def test_indicator_subcolecction_item(self):
        datasource_json = json.dumps(dict(
           id=1,
           id_source='1',
           name='World Bank 1',
           organization_id=1
        ))
        indicator_json = json.dumps(dict(
           id=1,
           name='donation',
           description='A gives a donation to B',
        ))
        dataset_json = json.dumps(dict(
           id=1,
           sdmx_frequency=1,
           datasource_id=1,
           license_id=1,
           indicators_id=['1']
        ))
        response = self.client.post("/datasources", data=datasource_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/datasources/1/indicators/1")
        self.assert404(response)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/datasets", data=dataset_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/datasources/1/indicators/1")
        self.assertEquals(response.json.get('id'), "1")
        response = self.client.delete("/datasources/1")
        self.assertStatus(response, 204)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/datasources/1")
        self.assert404(response)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/datasources")
        self.assertStatus(response, 204)
        response = self.client.get("/datasources")
        self.assert200(response)
        datasources = response.json
        self.assertEquals(len(datasources), 0)
        response = self.client.delete("/datasets")
        self.assertStatus(response, 204)
        response = self.client.get("/datasets")
        self.assert200(response)
        datasets = response.json
        self.assertEquals(len(datasets), 0)

    def test_indicator_subcolecction_collection(self):
        datasource_json = json.dumps(dict(
           id=1,
           id_source='1',
           name='World Bank 1',
           organization_id=1
        ))
        indicator_json = json.dumps(dict(
           id=1,
           name='donation',
           description='A gives a donation to B',
        ))
        indicator2_json = json.dumps(dict(
           id=2,
           name='donation',
           description='B gives a donation to A',
        ))
        dataset_json = json.dumps(dict(
           id='1',
           sdmx_frequency=1,
           datasource_id=1,
           license_id=1,
           indicators_id=['1']
        ))
        dataset2_json = json.dumps(dict(
           id='2',
           sdmx_frequency=1,
           datasource_id=1,
           license_id=2,
           indicators_id=['2']
        ))
        response = self.client.post("/datasources", data=datasource_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/datasources/1/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/datasets", data=dataset_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/datasets", data=dataset2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/datasources/1/indicators")
        indicator = response.json[0]
        indicator2 = response.json[1]
        self.assertEquals(indicator['id'], "1")
        self.assertEquals(indicator2['id'], "2")
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/datasources")
        self.assertStatus(response, 204)
        response = self.client.get("/datasources")
        self.assert200(response)
        datasources = response.json
        self.assertEquals(len(datasources), 0)
        response = self.client.delete("/datasets")
        self.assertStatus(response, 204)
        response = self.client.get("/datasets")
        self.assert200(response)
        datasets = response.json
        self.assertEquals(len(datasets), 0)


class TestDataset(ApiTest):
    def test_item(self):
        dataset_json = json.dumps(dict(
           id=1,
           sdmx_frequency=1,
           datasource_id=1,
           license_id=1
        ))
        dataset_updated = json.dumps(dict(
           id=1,
           sdmx_frequency=2,
           datasource_id=2,
           license_id=2
        ))
        response = self.client.get("/datasets/1")
        self.assert404(response)
        response = self.client.post("/datasets", data=dataset_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/datasets/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('sdmx_frequency'), '1')
        self.assertEquals(response.json.get('datasource_id'), 1)
        self.assertEquals(response.json.get('license_id'), 1)
        response = self.client.put("/datasets/1", data=dataset_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/datasets/1")
        self.assertEquals(response.json.get('sdmx_frequency'), '2')
        self.assertEquals(response.json.get('datasource_id'), 2)
        self.assertEquals(response.json.get('license_id'), 2)
        response = self.client.delete("/datasets/1")
        self.assertStatus(response, 204)
        response = self.client.get("/datasets/1")
        self.assert404(response)

    def test_collection(self):
        dataset_json = json.dumps(dict(
           id=1,
           sdmx_frequency=1,
           datasource_id=1,
           license_id=1
        ))
        dataset2_json = json.dumps(dict(
           id=2,
           sdmx_frequency=2,
           datasource_id=2,
           license_id=2
        ))
        datasets_updated = json.dumps([
            dict(id=1, sdmx_frequency=3, datasource_id=3, license_id=3),
            dict(id=2, sdmx_frequency=4, datasource_id=4, license_id=4)
        ])
        response = self.client.get("/datasets")
        self.assert200(response)
        datasources = response.json
        self.assertEquals(len(datasources), 0)
        response = self.client.post("/datasets", data=dataset_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/datasets", data=dataset2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/datasets")
        dataset = response.json[0]
        dataset2 = response.json[1]
        self.assertEquals(dataset['id'], 1)
        self.assertEquals(dataset['sdmx_frequency'], '1')
        self.assertEquals(dataset['datasource_id'], 1)
        self.assertEquals(dataset['license_id'], 1)
        self.assertEquals(dataset2['id'], 2)
        self.assertEquals(dataset2['sdmx_frequency'], '2')
        self.assertEquals(dataset2['datasource_id'], 2)
        self.assertEquals(dataset2['license_id'], 2)
        response = self.client.put("/datasets", data=datasets_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/datasets")
        dataset = response.json[0]
        dataset2 = response.json[1]
        self.assertEquals(dataset['sdmx_frequency'], '3')
        self.assertEquals(dataset['datasource_id'], 3)
        self.assertEquals(dataset['license_id'], 3)
        self.assertEquals(dataset2['sdmx_frequency'], '4')
        self.assertEquals(dataset2['datasource_id'], 4)
        self.assertEquals(dataset2['license_id'], 4)
        response = self.client.delete("/datasets")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/datasets")
        self.assert200(response)
        datasources = response.json
        self.assertEquals(len(datasources), 0)


class TestObservationBy(ApiTest):
    def test_get_by_country(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        response = self.client.get("/observations/ESP")
        self.assert404(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/ESP")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 1)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 1)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.get("/observations/ESP")
        self.assert404(response)

    def test_get_by_indicator(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        indicator_json = json.dumps(dict(
           id='1',
           name='donation',
           description='A gives a donation to B',
        ))
        dataset_json = json.dumps(dict(
           id=1,
           sdmx_frequency=1,
           datasource_id=1,
           license_id=1,
           indicators_id=['1']
        ))
        response = self.client.get("/observations/1")
        self.assert404(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/datasets", data=dataset_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/1")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 1)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 1)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.delete("/datasets")
        self.assertStatus(response, 204)
        response = self.client.get("/observations/1")
        self.assert404(response)

    def test_get_by_region(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           id=1,
           is_part_of_id=2
        ))
        region_json = json.dumps(dict(
            id=2,
            un_code='200',
            name='Europe'
        ))
        response = self.client.get("/observations/200")
        self.assert404(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/200")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 1)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 1)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.delete("/regions")
        self.assertStatus(response, 204)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.get("/observations/200")
        self.assert404(response)

    def test_get_by_country_and_indicator(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id="1",
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        indicator_json = json.dumps(dict(
           id="1",
           name='donation',
           description='A gives a donation to B',
           dataset_id=1
        ))
        response = self.client.get("/observations/ESP/1")
        self.assert400(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/ESP/1")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 1)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 1)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/observations/ESP/1")
        self.assert400(response)

    def test_get_by_indicator_and_country(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        indicator_json = json.dumps(dict(
           id=1,
           name='donation',
           description='A gives a donation to B',
           dataset_id=1
        ))
        response = self.client.get("/observations/1/ESP")
        self.assert400(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/1/ESP")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 1)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 1)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/observations/1/ESP")
        self.assert400(response)

    def test_get_by_region_and_indicator(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=1,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           id=1,
           is_part_of_id=2
        ))
        region_json = json.dumps(dict(
            id=2,
            un_code=200,
            name='Europe'
        ))
        indicator_json = json.dumps(dict(
           id=1,
           name='donation',
           description='A gives a donation to B',
           dataset_id=1
        ))
        response = self.client.get("/observations/200/1")
        self.assert400(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/200/1")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 1)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 1)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.delete("/regions")
        self.assertStatus(response, 204)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.get("/observations/200/1")
        self.assert400(response)


class TestValue(ApiTest):
    def test_item(self):
        value_json = json.dumps(dict(
           id=1,
           value='100'
        ))
        value_updated = json.dumps(dict(
            id=1,
            value='2000'
        ))
        response = self.client.get("/values/1")
        self.assert404(response)
        response = self.client.post("/values", data=value_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/values/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('value'), "100")
        response = self.client.put("/values/1", data=value_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/values/1")
        self.assertEquals(response.json.get('value'), "2000")
        response = self.client.delete("/values/1")
        self.assertStatus(response, 204)
        response = self.client.get("/values/1")
        self.assert404(response)

    def test_collection(self):
        value_json = json.dumps(dict(
           id=1,
           value='100'
        ))
        value2_json = json.dumps(dict(
            id=2,
            value='2000'
        ))
        values_updated = json.dumps([
            dict(id=1, value='1000'),
            dict(id=2, value='200')
        ])
        response = self.client.get("/values")
        self.assert200(response)
        values = response.json
        self.assertEquals(len(values), 0)
        response = self.client.post("/values", data=value_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/values", data=value2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/values")
        value1 = response.json[0]
        value2 = response.json[1]
        self.assertEquals(value1['id'], 1)
        self.assertEquals(value1['value'], "100")
        self.assertEquals(value2['id'], 2)
        self.assertEquals(value2['value'], "2000")
        response = self.client.put("/values", data=values_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/values")
        value1 = response.json[0]
        value2 = response.json[1]
        self.assertEquals(value1['value'], "1000")
        self.assertEquals(value2['value'], "200")
        response = self.client.delete("/values")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/values")
        self.assert200(response)
        values = response.json
        self.assertEquals(len(values), 0)


class TestTopic(ApiTest):
    def test_item(self):
        topic_json = json.dumps(dict(
           name='Land rights',
           id=1
        ))
        topic_updated = json.dumps(dict(
            name='Rural indicators',
            id=1
        ))
        response = self.client.get("/topics/1")
        self.assert404(response)
        response = self.client.post("/topics", data=topic_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/topics/1")
        self.assertEquals(response.json.get('id'), "1")
        response = self.client.put("/topics/1", data=topic_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/topics/1")
        self.assertEquals(response.json.get('id'), "1")
        response = self.client.delete("/topics/1")
        self.assertStatus(response, 204)
        response = self.client.get("/topics/1")
        self.assert404(response)

    def test_collection(self):
        topic_json = json.dumps(dict(
           name='Land rights',
           id=1
        ))
        topic2_json = json.dumps(dict(
            name='Rural indicators',
            id=2
        ))
        topics_updated = json.dumps([
            dict(name='Land', id=1),
            dict(name='Rural', id=2)
        ])
        response = self.client.get("/topics")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/topics", data=topic_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/topics", data=topic2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/topics")
        self.assertEquals(len(response.json), 2)
        response = self.client.put("/topics", data=topics_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/topics")
        self.assertEquals(len(response.json), 2)
        response = self.client.delete("/topics")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/topics")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_indicator_subcolecction_item(self):
        topic_json = json.dumps(dict(
           name='Land rights',
           id='1',
        ))
        indicator_json = json.dumps(dict(
           id='1',
           name='donation',
           description='A gives a donation to B',
           topic_id='1'
        ))
        response = self.client.post("/topics", data=topic_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/topics/1/indicators/1")
        self.assert404(response)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/topics/1/indicators/1")
        self.assertEquals(response.json.get('id'), "1")
        response = self.client.delete("/topics/1")
        self.assertStatus(response, 204)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/topics/1")
        self.assert404(response)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/topics")
        self.assertStatus(response, 204)
        response = self.client.get("/topics")
        self.assert200(response)
        topics = response.json
        self.assertEquals(len(topics), 0)

    def test_user_subcolecction_collection(self):
        topic_json = json.dumps(dict(
           name='Land rights',
           id='1'
        ))
        indicator1_json = json.dumps(dict(
           id='1',
           name='donation',
           description='A gives a donation to B',
           topic_id='1'
        ))
        indicator2_json = json.dumps(dict(
           id='2',
           name='donationB',
           description='B gives a donation to A',
           topic_id='1'
        ))
        response = self.client.post("/topics", data=topic_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/topics/1/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=indicator1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/topics/1/indicators")
        indicator = response.json[0]
        indicator2 = response.json[1]
        self.assertEquals(indicator['id'], "1")
        self.assertEquals(indicator2['id'], "2")
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/topics")
        self.assertStatus(response, 204)
        response = self.client.get("/topics")
        self.assert200(response)
        topics = response.json
        self.assertEquals(len(topics), 0)


class TestLastUpdate(ApiTest):
    def test_by_country(self):
        time_now = time()
        indicator1_json = json.dumps(dict(
            id=1,
            name='donation',
            description='donation from A to B',
            last_update=time_now-1e8
        ))
        indicator2_json = json.dumps(dict(
            id=2,
            name='receiver',
            description='receives a donation from B',
            last_update=time_now
        ))
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           id=1
        ))
        observation_json = json.dumps(dict(
           id=1,
           id_source=1,
           indicator_id=1,
           region_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           id_source=2,
           indicator_id=2,
           region_id=1
        ))
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=indicator1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/countries/ESP/last_update")
        last_update = response.json
        self.assertEquals(last_update['last_update'], long(time_now))
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)

    def test_by_indicator_and_country(self):
        time_now = time()
        indicator1_json = json.dumps(dict(
            id=1,
            name='donation',
            description='donation from A to B',
            last_update=time_now-1e8
        ))
        indicator2_json = json.dumps(dict(
            id=2,
            name='receiver',
            description='receives a donation from B',
            last_update=time_now
        ))
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           id=1
        ))
        observation_json = json.dumps(dict(
           id=1,
           id_source=1,
           indicator_id=1,
           region_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           id_source=2,
           indicator_id=2,
           region_id=1
        ))
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/indicators", data=indicator1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/1/ESP/last_update")
        last_update = response.json
        self.assertEquals(last_update['last_update'], long(time_now - 1e8))
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)


class TestObservationByPeriod(ApiTest):
    def test_get_by_country(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=2,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=3,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        time_object = models.Interval()
        time_object.id = 2
        time_object.start_time = datetime(2012, 06, 12)
        time_object.end_time = datetime(2014, 04, 01)
        app.db.session.add(time_object)
        response = self.client.get("/observations/ESP")
        self.assert404(response)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/ESP/range?from=20120611&to=20140402")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 2)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 3)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.get("/observations/ESP/range?from=20140402&to=20140403")
        self.assertEquals(len(response.json), 0)
        response = self.client.get("/observations/ESP/range?from=20120609&to=20120610")
        self.assertEquals(len(response.json), 0)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.get("/observations/ESP")
        self.assert404(response)

    def test_get_by_indicator(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=2,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=1,
           slice_id=1
        ))
        indicator_json = json.dumps(dict(
           id=1,
           name='donation',
           description='A gives a donation to B',
        ))
        dataset_json = json.dumps(dict(
           id=1,
           sdmx_frequency=1,
           datasource_id=1,
           license_id=1,
           indicators_id=['1']
        ))
        time_object = models.Interval()
        time_object.id = 2
        time_object.start_time = datetime(2012, 06, 12)
        time_object.end_time = datetime(2014, 04, 01)
        app.db.session.add(time_object)
        response = self.client.get("/observations/1")
        self.assert404(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/datasets", data=dataset_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/1/range?from=20120611&to=20140402")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 2)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 1)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.get("/observations/1/range?from=20140402&to=20140403")
        self.assertEquals(len(response.json), 0)
        response = self.client.get("/observations/1/range?from=20120609&to=20120610")
        self.assertEquals(len(response.json), 0)
        response = self.client.get("/observations/1/range?from=20140401&to=20140410")
        self.assertEquals(len(response.json), 1)
        response = self.client.get("/observations/1/range?from=20140602&to=20140603")
        self.assertEquals(len(response.json), 0)
        response = self.client.get("/observations/1")
        self.assertEquals(len(response.json), 1)
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.delete("/datasets")
        self.assertStatus(response, 204)
        response = self.client.get("/observations/1")
        self.assert404(response)

    def test_get_by_region(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=3,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id=1,
           dataset_id=1,
           region_id=4,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP',
           id=1,
           is_part_of_id=2
        ))
        region_json = json.dumps(dict(
            id=2,
            un_code='200',
            name='Europe'
        ))
        time_object = models.Interval()
        time_object.id = 3
        time_object.start_time = datetime(2012, 06, 12)
        time_object.end_time = datetime(2014, 04, 01)
        app.db.session.add(time_object)
        response = self.client.get("/observations/2")
        self.assert404(response)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions", data=region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/observations/200/range?from=20120611&to=20140402")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 3)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "1")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 4)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.get("/observations/200/range?from=20140402&to=20140403")
        self.assertEquals(len(response.json), 0)
        response = self.client.get("/observations/200/range?from=20120609&to=20120610")
        self.assertEquals(len(response.json), 0)
        response = self.client.delete("/observations")
        self.assertStatus(response, 204)
        response = self.client.delete("/regions")
        self.assertStatus(response, 204)
        response = self.client.delete("/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/countries")
        self.assert200(response)
        observations = response.json
        self.assertEquals(len(observations), 0)
        response = self.client.get("/observations/200")
        self.assert404(response)


class TestIndicatorByPeriod(ApiTest):
    def test_get_by_range(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=2,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id='HDI',
           dataset_id=1,
           region_id=3,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        indicator_json = json.dumps(dict(
            id='HDI',
            name='HDI'
        ))
        time_object = models.Interval()
        time_object.id = 2
        time_object.start_time = datetime(2012, 06, 12)
        time_object.end_time = datetime(2014, 04, 01)
        app.db.session.add(time_object)
        response = self.client.get("/observations/ESP")
        self.assert404(response)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/HDI/range?from=20120611&to=20140402")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 2)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "HDI")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 3)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.get("/indicators/HDI/range?from=20140402&to=20140403")
        self.assertEquals(len(response.json), 0)
        response = self.client.get("/indicators/HDI/range?from=20120609&to=20120610")
        self.assertEquals(len(response.json), 0)

    def test_get_average_by_range(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=2,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id='HDI',
           dataset_id=1,
           region_id=3,
           slice_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           ref_time_id=2,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=2,
           indicator_id='HDI',
           dataset_id=1,
           region_id=3,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        indicator_json = json.dumps(dict(
            id='HDI',
            name='HDI'
        ))
        value1_json = json.dumps(dict(
            id=1,
            value=50
        ))
        value2_json = json.dumps(dict(
            id=2,
            value=100
        ))
        time_object = models.Interval()
        time_object.id = 2
        time_object.start_time = datetime(2012, 06, 12)
        time_object.end_time = datetime(2014, 04, 01)
        app.db.session.add(time_object)
        response = self.client.get("/observations/ESP")
        self.assert404(response)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/values", data=value1_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/values", data=value2_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/indicators/HDI/average/range?from=20120611&to=20140402")
        self.assertEquals(response.json['value'], 75)
        response = self.client.get("/indicators/HDI/average/range?from=20140402&to=20140403")
        self.assert404(response)
        response = self.client.get("/indicators/HDI/average/range?from=20120609&to=20120610")
        self.assert404(response)

    def test_get_by_country_and_range(self):
        observation_json = json.dumps(dict(
           id=1,
           ref_time_id=2,
           issued_id=1,
           computation_id=1,
           indicator_group_id=1,
           value_id=1,
           indicator_id='HDI',
           dataset_id=1,
           region_id=3,
           slice_id=1
        ))
        country_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        indicator_json = json.dumps(dict(
            id='HDI',
            name='HDI'
        ))
        time_object = models.Interval()
        time_object.id = 2
        time_object.start_time = datetime(2012, 06, 12)
        time_object.end_time = datetime(2014, 04, 01)
        app.db.session.add(time_object)
        response = self.client.get("/observations/ESP")
        self.assert404(response)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/HDI/ESP/range?from=20120611&to=20140402")
        observation = response.json[0]
        self.assertEquals(observation['id'], "1")
        self.assertEquals(observation['ref_time_id'], 2)
        self.assertEquals(observation['issued_id'], 1)
        self.assertEquals(observation['computation_id'], 1)
        self.assertEquals(observation['indicator_group_id'], '1')
        self.assertEquals(observation['value_id'], 1)
        self.assertEquals(observation['indicator_id'], "HDI")
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation['region_id'], 3)
        self.assertEquals(observation['slice_id'], "1")
        response = self.client.get("/indicators/HDI/ESP/range?from=20140402&to=20140403")
        self.assertEquals(len(response.json), 0)
        response = self.client.get("/indicators/HDI/ESP/range?from=20120609&to=20120610")
        self.assertEquals(len(response.json), 0)


class TestRelatedIndicator(ApiTest):
    def test_indicator_subcolecction_collection(self):
        indicator_json = json.dumps(dict(
           id='HDI',
           name='donation',
           description='A gives a donation to B'
        ))
        indicator2_json = json.dumps(dict(
           id='DHI',
           name='donation',
           description='B gives a donation to A'
        ))
        response = self.client.get("/indicators/HDI/related")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        is_part_of_object = models.IsPartOf()
        is_part_of_object.source_id = 'HDI'
        is_part_of_object.target_id = 'DHI'
        app.db.session.add(is_part_of_object)
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/HDI/related")
        indicator = response.json[0]
        self.assertEquals(indicator['id'], "DHI")
        response = self.client.delete("/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)


class TestIndicatorCountryTendency(ApiTest):
    def test_get_indicator_country_tendency(self):
        country_json = json.dumps(dict(
           iso2='ES',
           iso3='ESP',
           id=1
        ))
        indicator_json = json.dumps(dict(
            id='HDI',
            name='HDI',
            preferable_tendency='Increase'
        ))
        observation_json = json.dumps(dict(
           id=1,
           indicator_id='HDI',
           region_id=1
        ))
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/HDI/ESP/tendency")
        self.assertEquals(response.json['tendency'], "Increase")


class TestTranslations(ApiTest):
    def test_region_translation_list(self):
        spain_translation_json = json.dumps(dict(
           name='Spain',
           lang_code='en',
           region_id=1
        ))
        france_translation_json = json.dumps(dict(
            name='France',
            lang_code='en',
            region_id=2
        ))
        spain_region_json = json.dumps(dict(
            id=1,
            iso3='ESP',
            iso2='ES'
        ))
        countries_translation_updated = json.dumps([
            dict(region_id=1, lang_code='en', name='SPA'),
            dict(region_id=2, lang_code='en', name='FRA')
        ])
        response = self.client.get("/regions/translations")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/countries", data=spain_region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions/translations", data=spain_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions/translations", data=france_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/regions/translations")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['name'], "Spain")
        self.assertEquals(spain['lang_code'], "en")
        self.assertEquals(france['name'], "France")
        self.assertEquals(france['lang_code'], "en")
        response = self.client.get("/countries/ESP")
        self.assertEqual(response.json.get('name'), 'Spain')
        response = self.client.put("/regions/translations", data=countries_translation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/regions/translations")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['name'], "SPA")
        self.assertEquals(france['name'], "FRA")
        response = self.client.delete("/regions/translations")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/regions/translations")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_region_translation_item(self):
        spain_translation_json = json.dumps(dict(
           name='Spain',
           lang_code='en',
           region_id=1
        ))
        spain_translation_updated = json.dumps(dict(
           name='SPA',
           lang_code='en',
           region_id=1
        ))
        spain_region_json = json.dumps(dict(
            id=1,
            un_code=200
        ))
        response = self.client.post("/regions", data=spain_region_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/regions/translations", data=spain_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/regions/translations/1/en")
        self.assertEquals(response.json.get('name'), "Spain")
        self.assertEquals(response.json.get('lang_code'), "en")
        response = self.client.get("/regions/200")
        self.assertEqual(response.json.get('name'), 'Spain')
        response = self.client.put("/regions/translations/1/en", data=spain_translation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/regions/translations/1/en")
        self.assertEquals(response.json.get('name'), "SPA")
        response = self.client.delete("/regions/translations/1/en")
        self.assertStatus(response, 204)
        response = self.client.get("/regions/translations/1/en")
        self.assert404(response)

    def test_indicator_translation_list(self):
        rp_translation_json = json.dumps(dict(
           name='Rural Population',
           description="Something",
           lang_code='EN',
           indicator_id='1'
        ))
        nrp_translation_json = json.dumps(dict(
            name='Non Rural Population',
            description="Anything",
            lang_code='EN',
            indicator_id='2'
        ))
        indicators_translation_updated = json.dumps([
            dict(indicator_id='1', lang_code='EN', description='Rural'),
            dict(indicator_id='2', lang_code='EN', description='Non Rural')
        ])
        response = self.client.get("/indicators/translations")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/indicators/translations", data=rp_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators/translations", data=nrp_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/indicators/translations")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['name'], "Rural Population")
        self.assertEquals(spain['description'], "Something")
        self.assertEquals(france['name'], "Non Rural Population")
        self.assertEquals(france['description'], "Anything")
        response = self.client.put("/indicators/translations", data=indicators_translation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/indicators/translations")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['description'], "Rural")
        self.assertEquals(france['description'], "Non Rural")
        response = self.client.delete("/indicators/translations")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/indicators/translations")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_indicator_translation_item(self):
        rp_translation_json = json.dumps(dict(
           name='Rural Population',
           description='Something',
           lang_code='en',
           indicator_id='1'
        ))
        rp_translation_update = json.dumps(dict(
           name='Rural Population',
           description='Anything',
           lang_code='en',
           indicator_id='1'
        ))
        indicator_json = json.dumps(dict(
            id='1',
        ))
        response = self.client.post("/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/indicators/translations", data=rp_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/indicators/translations/1/en")
        self.assertEquals(response.json.get('name'), "Rural Population")
        self.assertEquals(response.json.get('description'), "Something")
        response = self.client.get("/indicators/1")
        self.assertEquals(response.json.get('name'), "Rural Population")
        self.assertEquals(response.json.get('description'), "Something")
        response = self.client.put("/indicators/translations/1/en", data=rp_translation_update, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/indicators/translations/1/en")
        self.assertEquals(response.json.get('description'), "Anything")
        response = self.client.delete("/indicators/translations/1/en")
        self.assertStatus(response, 204)
        response = self.client.get("/indicators/translations/1/en")
        self.assert404(response)

    def test_topic_translation_list(self):
        topic1_translation_json = json.dumps(dict(
           name='Topic1',
           lang_code='EN',
           topic_id='1'
        ))
        topic2_translation_json = json.dumps(dict(
            name='Topic2',
            lang_code='EN',
            topic_id='2'
        ))
        topics_translation_updated = json.dumps([
            dict(topic_id='1', lang_code='EN', name='TopicA'),
            dict(topic_id='2', lang_code='EN', name='TopicB')
        ])
        response = self.client.get("/topics/translations")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/topics/translations", data=topic1_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/topics/translations", data=topic2_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        app.cache.clear()
        response = self.client.get("/topics/translations")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['name'], "Topic1")
        self.assertEquals(france['name'], "Topic2")
        response = self.client.put("/topics/translations", data=topics_translation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/topics/translations")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['name'], "TopicA")
        self.assertEquals(france['name'], "TopicB")
        response = self.client.delete("/topics/translations")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/topics/translations")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_topic_translation_item(self):
        topic1_translation_json = json.dumps(dict(
           name='Topic1',
           lang_code='en',
           topic_id='1'
        ))
        topic1_translation_update = json.dumps(dict(
           name='TopicA',
           lang_code='en',
           topic_id='1'
        ))
        topic_json = json.dumps(dict(
            id='1',
        ))
        response = self.client.post("/topics", data=topic_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/topics/translations", data=topic1_translation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/topics/translations/1/en")
        self.assertEquals(response.json.get('name'), "Topic1")
        response = self.client.get("/topics/1")
        self.assertEquals(response.json.get('translation_name'), "Topic1")
        response = self.client.put("/topics/translations/1/en", data=topic1_translation_update, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/topics/translations/1/en")
        self.assertEquals(response.json.get('name'), "TopicA")
        response = self.client.delete("/topics/translations/1/en")
        self.assertStatus(response, 204)
        app.cache.clear()
        response = self.client.get("/topics/translations/1/en")
        self.assert404(response)


class TestCSV(ApiTest):
    def test_csv(self):
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        response = self.client.get("/countries/ESP?format=csv")
        self.assert404(response)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/countries/ESP?format=csv")
        self.assertEquals(response.data, "is_part_of_id;type;faoURI;iso3;iso2;un_code;id\nNone;countries;None;ESP;ES;None;1;\n")


class TestJSONP(ApiTest):
    def test_jsonp(self):
        topic_json = json.dumps(dict(
           lang_code='en',
           topic_id='1',
           name='Topic'
        ))
        response = self.client.get("/topics/translations/1/en?format=jsonp")
        self.assert404(response)
        response = self.client.post("/topics/translations", data=topic_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/topics/translations/1/en?format=jsonp")
        self.assertEquals(response.data, "callback(" + topic_json + ");")


class LocalhostTest(ApiTest):
    def create_app(self):
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
        app.app.config['TESTING'] = True
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///foo.db'
        return app.app

    def test(self):
        spain_json = json.dumps(dict(
           name='Spain',
           iso2='ES',
           iso3='ESP'
        ))
        response = self.client.get("/countries/ESP")
        self.assert401(response)
        response = self.client.post("/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 403)


if __name__ == '__main__':
    unittest.main()
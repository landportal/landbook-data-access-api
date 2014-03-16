__author__ = 'Herminio'

import unittest
import app
from flask_testing import TestCase
from app.utils import JSONConverter
import json

json_converter = JSONConverter()


class ApiTest(TestCase):
    """
    Generic class for all test concerning Flask on this API
    """
    def create_app(self):
        app.app.config['TESTING'] = True
        return app.app

    def setUp(self):
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
            name='Espagne',
            iso2='ES'
        ))
        response = self.client.get("/api/countries/ESP")
        self.assert404(response)
        response = self.client.post("/api/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/countries/ESP")
        self.assertEquals(response.json.get('name'), "Spain")
        self.assertEquals(response.json.get('iso2'), "ES")
        self.assertEquals(response.json.get('iso3'), "ESP")
        response = self.client.put("/api/countries/ESP", data=spain_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/countries/ESP")
        self.assertEquals(response.json.get('name'), "Espagne")
        response = self.client.delete("/api/countries/ESP")
        self.assertStatus(response, 204)
        response = self.client.get("/api/countries/ESP")
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
            dict(name='Espagne', iso2='ES', iso3='ESP'),
            dict(name='France', iso2='FR', iso3='FRA')
        ])
        response = self.client.get("/api/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)
        response = self.client.post("/api/countries", data=spain_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/countries", data=france_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/countries")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['name'], "Spain")
        self.assertEquals(spain['iso2'], "ES")
        self.assertEquals(spain['iso3'], "ESP")
        self.assertEquals(france['name'], "France")
        self.assertEquals(france['iso2'], "FR")
        self.assertEquals(france['iso3'], "FRA")
        response = self.client.put("/api/countries", data=countries_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/countries")
        spain = response.json[0]
        france = response.json[1]
        self.assertEquals(spain['name'], "Espagne")
        self.assertEquals(france['name'], "France")
        response = self.client.delete("/api/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/api/countries")
        self.assert200(response)
        countries = response.json
        self.assertEquals(len(countries), 0)

    def test_indicator_subcolecction_item(self):
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
        observation_json = json.dumps(dict(
           id=1,
           id_source=1,
           indicator_id=1,
           region_id=1
        ))
        response = self.client.post("/api/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/countries/ESP/indicators/1")
        self.assert404(response)
        response = self.client.post("/api/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/countries/ESP/indicators/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('name'), "donation")
        self.assertEquals(response.json.get('description'), "A gives a donation to B")
        response = self.client.delete("/api/countries/ESP")
        self.assertStatus(response, 204)
        response = self.client.delete("/api/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/api/countries/ESP")
        self.assert404(response)
        response = self.client.get("/api/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/api/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/api/countries")
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
        response = self.client.post("/api/countries", data=country_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/countries/ESP/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/api/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/indicators", data=indicator2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/countries/ESP/indicators")
        indicator = response.json[0]
        indicator2 = response.json[1]
        self.assertEquals(indicator['id'], 1)
        self.assertEquals(indicator['name'], "donation")
        self.assertEquals(indicator['description'], "A gives a donation to B")
        self.assertEquals(indicator2['id'], 2)
        self.assertEquals(indicator2['name'], "donation")
        self.assertEquals(indicator2['description'], "B gives a donation to A")
        response = self.client.delete("/api/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/api/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.delete("/api/countries")
        self.assertStatus(response, 204)
        response = self.client.get("/api/countries")
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
        response = self.client.get("/api/indicators/1")
        self.assert404(response)
        response = self.client.post("/api/indicators", data=indicator_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/indicators/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('name'), "donation")
        self.assertEquals(response.json.get('description'), "donation from A to B")
        response = self.client.put("/api/indicators/1", data=indicator_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/indicators/1")
        self.assertEquals(response.json.get('description'), "donation from B to A")
        response = self.client.delete("/api/indicators/1")
        self.assertStatus(response, 204)
        response = self.client.get("/api/indicators/1")
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
        response = self.client.get("/api/indicators")
        self.assert200(response)
        indicators = response.json
        self.assertEquals(len(indicators), 0)
        response = self.client.post("/api/indicators", data=donation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/indicators", data=receiver_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/indicators")
        donation = response.json[0]
        receiver = response.json[1]
        self.assertEquals(donation['id'], 1)
        self.assertEquals(donation['name'], "donation")
        self.assertEquals(donation['description'], "donation from A to B")
        self.assertEquals(receiver['id'], 2)
        self.assertEquals(receiver['name'], "receiver")
        self.assertEquals(receiver['description'], "receives a donation from B")
        response = self.client.put("/api/indicators", data=indicators_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/indicators")
        donation = response.json[0]
        receiver = response.json[1]
        self.assertEquals(donation['description'], "donation from B to A")
        self.assertEquals(receiver['description'], "receives a donation from A")
        response = self.client.delete("/api/indicators")
        self.assertStatus(response, 204)
        response = self.client.get("/api/indicators")
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
        response = self.client.get("/api/users/1")
        self.assert404(response)
        response = self.client.post("/api/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/users/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('ip'), "192.168.1.1")
        response = self.client.put("/api/users/1", data=user_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/users/1")
        self.assertEquals(response.json.get('ip'), "192.168.1.2")
        response = self.client.delete("/api/users/1")
        self.assertStatus(response, 204)
        response = self.client.get("/api/users/1")
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
        response = self.client.get("/api/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.post("/api/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/users", data=user2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/users")
        user = response.json[0]
        user2 = response.json[1]
        self.assertEquals(user['id'], 1)
        self.assertEquals(user['ip'], "192.168.1.1")
        self.assertEquals(user2['id'], 2)
        self.assertEquals(user2['ip'], "192.168.1.2")
        response = self.client.put("/api/users", data=users_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/users")
        user = response.json[0]
        user2 = response.json[1]
        self.assertEquals(user['ip'], "192.168.1.3")
        self.assertEquals(user2['ip'], "192.168.1.4")
        response = self.client.delete("/api/users")
        self.assertStatus(response, 204)
        response = self.client.get("/api/users")
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
        response = self.client.get("/api/organizations/1")
        self.assert404(response)
        response = self.client.post("/api/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/organizations/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('name'), "Organization A")
        self.assertEquals(response.json.get('url'), "http://www.organizationA.com")
        response = self.client.put("/api/organizations/1", data=organization_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/organizations/1")
        self.assertEquals(response.json.get('name'), "Organization B")
        self.assertEquals(response.json.get('url'), "http://www.organizationB.com")
        response = self.client.delete("/api/organizations/1")
        self.assertStatus(response, 204)
        response = self.client.get("/api/organizations/1")
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
        response = self.client.get("/api/organizations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)
        response = self.client.post("/api/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/organizations", data=organization2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/organizations")
        organization = response.json[0]
        organization2 = response.json[1]
        self.assertEquals(organization['id'], 1)
        self.assertEquals(organization['name'], "Organization A")
        self.assertEquals(organization['url'], "http://www.organizationA.com")
        self.assertEquals(organization2['id'], 2)
        self.assertEquals(organization2['name'], "Organization B")
        self.assertEquals(organization2['url'], "http://www.organizationB.com")
        response = self.client.put("/api/organizations", data=organizations_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/organizations")
        organization = response.json[0]
        organization2 = response.json[1]
        self.assertEquals(organization['name'], "Organization C")
        self.assertEquals(organization['url'], "http://www.organizationC.com")
        self.assertEquals(organization2['name'], "Organization D")
        self.assertEquals(organization2['url'], "http://www.organizationD.com")
        response = self.client.delete("/api/organizations")
        self.assertStatus(response, 204)
        response = self.client.get("/api/organizations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

    def test_user_subcolecction_item(self):
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
        response = self.client.post("/api/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/organizations/1/users/1")
        self.assert404(response)
        response = self.client.post("/api/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/organizations/1/users/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('ip'), "192.168.1.1")
        response = self.client.delete("/api/organizations/1")
        self.assertStatus(response, 204)
        response = self.client.delete("/api/users")
        self.assertStatus(response, 204)
        response = self.client.get("/api/organizations/1")
        self.assert404(response)
        response = self.client.get("/api/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.delete("/api/organizations")
        self.assertStatus(response, 204)
        response = self.client.get("/api/organizations")
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
        response = self.client.post("/api/organizations", data=organization_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/organizations/1/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.post("/api/users", data=user_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/users", data=user2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/organizations/1/users")
        user = response.json[0]
        user2 = response.json[1]
        self.assertEquals(user['id'], 1)
        self.assertEquals(user['ip'], "192.168.1.1")
        self.assertEquals(user2['id'], 2)
        self.assertEquals(user2['ip'], "192.168.1.2")
        response = self.client.delete("/api/users")
        self.assertStatus(response, 204)
        response = self.client.get("/api/users")
        self.assert200(response)
        users = response.json
        self.assertEquals(len(users), 0)
        response = self.client.delete("/api/organizations")
        self.assertStatus(response, 204)
        response = self.client.get("/api/organizations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)


class TestObservation(ApiTest):
    def test_item(self):
        observation_json = json.dumps(dict(
           id=1,
           id_source=1,
           dataset_id=1
        ))
        observation_updated = json.dumps(dict(
           id=1,
           id_source=2,
           dataset_id=2
        ))
        response = self.client.get("/api/observations/1")
        self.assert404(response)
        response = self.client.post("/api/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/observations/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('id_source'), '1')
        self.assertEquals(response.json.get('dataset_id'), 1)
        response = self.client.put("/api/observations/1", data=observation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/observations/1")
        self.assertEquals(response.json.get('id'), 1)
        self.assertEquals(response.json.get('id_source'), '2')
        self.assertEquals(response.json.get('dataset_id'), 2)
        response = self.client.delete("/api/observations/1")
        self.assertStatus(response, 204)
        response = self.client.get("/api/observations/1")
        self.assert404(response)

    def test_collection(self):
        observation_json = json.dumps(dict(
           id=1,
           id_source=1,
           dataset_id=1
        ))
        observation2_json = json.dumps(dict(
           id=2,
           id_source=2,
           dataset_id=2
        ))
        observation_updated = json.dumps([
            dict(id=1, id_source=2, dataset_id=2),
            dict(id=2, id_source=1, dataset_id=1)
        ])
        response = self.client.get("/api/observations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)
        response = self.client.post("/api/observations", data=observation_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.post("/api/observations", data=observation2_json, content_type='application/json')
        self.assertStatus(response, 201)
        response = self.client.get("/api/observations")
        observation = response.json[0]
        observation2 = response.json[1]
        self.assertEquals(observation['id'], 1)
        self.assertEquals(observation['id_source'], '1')
        self.assertEquals(observation['dataset_id'], 1)
        self.assertEquals(observation2['id'], 2)
        self.assertEquals(observation2['id_source'], '2')
        self.assertEquals(observation2['dataset_id'], 2)
        response = self.client.put("/api/observations", data=observation_updated, content_type='application/json')
        self.assertStatus(response, 204)
        response = self.client.get("/api/observations")
        observation = response.json[0]
        observation2 = response.json[1]
        self.assertEquals(observation['id'], 1)
        self.assertEquals(observation['id_source'], '2')
        self.assertEquals(observation['dataset_id'], 2)
        self.assertEquals(observation2['id'], 2)
        self.assertEquals(observation2['id_source'], '1')
        self.assertEquals(observation2['dataset_id'], 1)
        response = self.client.delete("/api/observations")
        self.assertStatus(response, 204)
        response = self.client.get("/api/observations")
        self.assert200(response)
        organizations = response.json
        self.assertEquals(len(organizations), 0)

if __name__ == '__main__':
    unittest.main()
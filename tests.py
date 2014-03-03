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


if __name__ == '__main__':
    unittest.main()
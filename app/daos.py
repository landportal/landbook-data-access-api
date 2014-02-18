'''
Created on 03/02/2014

@author: Herminio
'''
from app.models import Country

class CountryDAO(object):
    '''
    Country DAO
    '''

    def set_session(self, session):
        '''
        Method to set the database to use
        '''
        self.session = session
        
    def get_all_countries(self):
        '''
        Method that returns all countries in the database
        '''
        return self.session.query(Country).all()
    
    def get_country_by_code(self, code):
        '''
        Method that returns a country by its given code
        '''
        return self.session.query(Country).filter_by(iso_code3=code).first()
    
    def insert_country(self, country):
        '''
        Method that inserts a new country
        '''
        self.session.add(country)
    
    def delete_country(self, code):
        '''
        Method to delete an existing country by its code
        '''
        country = self.get_country_by_code(code)
        self.session.delete(country)
        
    def update_country(self, country):
        '''
        Method to update an existing country, its code will not be changed
        '''
        persisted_country = self.get_country_by_code(country.iso_code3)
        for attr in dir(persisted_country):
            if hasattr(country, attr) and attr[0] is not "_" :
                setattr(persisted_country, attr, getattr(country, attr))
        print persisted_country.faoURI
        print country.faoURI

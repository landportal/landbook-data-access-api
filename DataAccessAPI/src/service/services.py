'''
Created on 03/02/2014

@author: Herminio
'''
import sqlite3 as dbapi
from src.dao.daos import CountryDAO

class CountryService(object):
    '''
    Service for country dao
    '''
    
    def __init__(self):
        '''
        Constructor for country service
        '''
        self.tm = TransactionManager()
        self.dao = CountryDAO()
    
    def get_all_countries(self):
        '''
        Method that returns all countries given by the dao
        '''
        return self.tm.execute(self.dao, self.dao.get_all_countries)
    
    def get_country_by_code(self, code):
        '''
        Method that returns country given by the dao
        '''
        return self.tm.execute(self.dao, self.dao.get_country_by_code, code)
    
    def insert_country(self, country):
        '''
        Method that inserts a country calling the dao
        '''
        self.tm.execute(self.dao, self.dao.insert_country, country)
    
    def delete_country(self, code):
        '''
        Method that deletes the country by its given code calling the dao
        '''
        self.tm.execute(self.dao, self.dao.delete_country, code)
        
    def update_country(self, country):
        '''
        Method that updates the country by calling the dao
        '''
        self.tm.execute(self.dao, self.dao.update_country, country)

    
    def delete_all_countries(self):
        '''
        Method that deletes all countries by calling the dao
        @attention: Take care of what you do, all countries will be destroyed
        '''
        self.tm.execute(self.dao, self.dao.delete_all_countries)
    
    def update_countries(self, countries):
        '''
        Method that updates all the countries given by calling the dao
        '''
        for country in countries:
            self.tm.execute(self.dao, self.dao.update_country, country)
    
    

class TransactionManager(object):
    '''
    Transaction manager that helps to abstract from the execution
    '''
    
    def execute(self, dao, function, *args):
        '''
        Abstraction for all calls to the dao methods, like command executor
        '''
        db = dbapi.connect('../../resources/DataAccessAPIdb.sqlite')
        getattr(dao, 'set_database')(db)
        result = function(*args)
        db.commit()
        db.close()
        return result
'''
Created on 03/02/2014

@author: Herminio
'''
from app.models import Country


class DAO(object):
    '''
    Generic DAO for all classes, only the class is needed
    '''
    def __init__(self, cls):
        self.cls = cls

    def set_session(self, session):
        '''
        Method to set the database to use
        '''
        self.session = session
        
    def get_all(self):
        '''
        Method that returns all countries in the database
        '''
        return self.session.query(self.cls).all()

    def get_by_code(self, code):
        '''
        Method that returns a country by its given code
        '''
        return self.session.query(self.cls).filter_by(id=code).first()
    
    def insert(self, object):
        '''
        Method that inserts a new country
        '''
        self.session.add(object)
    
    def delete(self, code):
        '''
        Method to delete an existing country by its code
        '''
        object = self.get_by_code(code)
        self.session.delete(object)

    def update(self, object):
        '''
        Method to update an existing country, its code will not be changed
        '''
        persisted_object = self.get_by_code(object.id)
        update_object_attributes(persisted_object, object)


class CountryDAO(DAO):
    def __init__(self):
        super(CountryDAO, self).__init__(Country)

    def get_by_code(self, code):
        '''
        Method that returns a country by its given code
        '''
        return self.session.query(self.cls).filter_by(iso3=code).first()

    def update(self, object):
        '''
        Method to update an existing country, its code will not be changed
        '''
        persisted_object = self.get_by_code(object.iso3)
        update_object_attributes(persisted_object, object)


def update_object_attributes(persisted_object, object):
    for attr in dir(persisted_object):
            if hasattr(object, attr) and attr[0] is not "_":
                setattr(persisted_object, attr, getattr(object, attr))
'''
Created on 03/02/2014

@author: Herminio
'''
from app import db
from daos import DAO, CountryDAO
from models import Country, Indicator, User, Organization


class GenericService(object):
    '''
    Service for country dao
    '''

    def __init__(self):
        '''
        Constructor for country service
        '''
        self.tm = TransactionManager()

    def get_all(self):
        '''
        Method that returns all countries given by the dao
        '''
        return self.tm.execute(self.dao, self.dao.get_all)

    def get_by_code(self, code):
        '''
        Method that returns country given by the dao
        '''
        return self.tm.execute(self.dao, self.dao.get_by_code, code)

    def insert(self, object):
        '''
        Method that inserts a country calling the dao
        '''
        self.tm.execute(self.dao, self.dao.insert, object)

    def delete(self, code):
        '''
        Method that deletes the country by its given code calling the dao
        '''
        self.tm.execute(self.dao, self.dao.delete, code)

    def update(self, object):
        '''
        Method that updates the country by calling the dao
        '''
        self.tm.execute(self.dao, self.dao.update, object)


    def delete_all(self):
        '''
        Method that deletes all countries by calling the dao
        @attention: Take care of what you do, all countries will be destroyed
        '''
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.id)

    def update_all(self, objects):
        '''
        Method that updates all the countries given by calling the dao
        '''
        for object in objects:
            self.tm.execute(self.dao, self.dao.update, object)

class CountryService(GenericService):
    '''
    Service for country dao
    '''
    
    def __init__(self):
        '''
        Constructor for country service
        '''
        super(CountryService, self).__init__()
        self.dao = CountryDAO()

    def delete_all(self):
        '''
        Method that deletes all countries by calling the dao
        @attention: Take care of what you do, all countries will be destroyed
        '''
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.iso3)

class IndicatorService(GenericService):
    '''
    Service for indicator dao
    '''
    def __init__(self):
        '''
        Constructor for indicator service
        '''
        super(IndicatorService, self).__init__()
        self.dao = DAO(Indicator)

class UserService(GenericService):
    """
    Service for user dao
    """
    def __init__(self):
        """
        Constructor for user service
        """
        super(UserService, self).__init__()
        self.dao = DAO(User)

class OrganizationService(GenericService):
    """
    Service for organization dao
    """
    def __init__(self):
        """
        Constructor for orgnization service
        """
        super(OrganizationService, self).__init__()
        self.dao = DAO(Organization)
    

class TransactionManager(object):
    '''
    Transaction manager that helps to abstract from the execution
    '''
    
    def execute(self, dao, function, *args):
        '''
        Abstraction for all calls to the dao methods, like command executor
        '''
        session = db.session
        getattr(dao, 'set_session')(session)
        result = function(*args)
        session.commit()
        
        return result




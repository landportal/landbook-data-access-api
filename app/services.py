'''
Created on 03/02/2014

@author: Herminio
'''
from app import db
from daos import DAO, CountryDAO, RegionTranslationDAO, IndicatorTranslationDAO, TopicTranslationDAO, RegionDAO
from model.models import Indicator, User, Organization, Observation, Region, DataSource, Dataset, Value, Topic, \
    IndicatorRelationship


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


class ObservationService(GenericService):
    """
    Service for organization dao
    """
    def __init__(self):
        """
        Constructor for orgnization service
        """
        super(ObservationService, self).__init__()
        self.dao = DAO(Observation)


class RegionService(GenericService):
    """
    Service for region dao
    """

    def __init__(self):
        super(RegionService, self).__init__()
        self.dao = RegionDAO()

    def delete_all(self):
        '''
        Method that deletes all countries by calling the dao
        @attention: Take care of what you do, all countries will be destroyed
        '''
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.un_code)


class DataSourceService(GenericService):
    """
    Service for DataSource dao
    """

    def __init__(self):
        super(DataSourceService, self).__init__()
        self.dao = DAO(DataSource)


class DatasetService(GenericService):
    """
    Service for Dataset dao
    """

    def __init__(self):
        super(DatasetService, self).__init__()
        self.dao = DAO(Dataset)

    def insert(self, dataset):
        self.indicator_dao = DAO(Indicator)
        dataset.indicators = []
        if dataset.indicators_id is not None:
            for indicator_id in dataset.indicators_id:
                indicator = self.tm.execute(self.indicator_dao, self.indicator_dao.get_by_code, indicator_id)
                if indicator is not None:
                    dataset.indicators.append(indicator)
        super(DatasetService, self).insert(dataset)


class ValueService(GenericService):
    """
    Service for Value dao
    """

    def __init__(self):
        super(ValueService, self).__init__()
        self.dao = DAO(Value)


class TopicService(GenericService):
    """
    Service for Topic dao
    """

    def __init__(self):
        super(TopicService, self).__init__()
        self.dao = DAO(Topic)


class IndicatorRelationshipService(GenericService):
    """
    Service for IsPartOf dao
    """

    def __init__(self):
        super(IndicatorRelationshipService, self).__init__()
        self.dao = DAO(IndicatorRelationship)


class RegionTranslationService(GenericService):
    """
    Service for region translation dao
    """

    def __init__(self):
        super(RegionTranslationService, self).__init__()
        self.dao = RegionTranslationDAO()

    def get_by_codes(self, region_id, lang_code):
        '''
        Method that returns country given by the dao
        '''
        return self.tm.execute(self.dao, self.dao.get_by_codes, region_id, lang_code)

    def delete(self, region_id, lang_code):
        '''
        Method that deletes the country by its given code calling the dao
        '''
        self.tm.execute(self.dao, self.dao.delete, region_id, lang_code)

    def delete_all(self):
        '''
        Method that deletes all countries by calling the dao
        @attention: Take care of what you do, all countries will be destroyed
        '''
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.region_id, object.lang_code)


class IndicatorTranslationService(GenericService):
    """
    Service for region translation dao
    """

    def __init__(self):
        super(IndicatorTranslationService, self).__init__()
        self.dao = IndicatorTranslationDAO()

    def get_by_codes(self, indicator_id, lang_code):
        '''
        Method that returns country given by the dao
        '''
        return self.tm.execute(self.dao, self.dao.get_by_codes, indicator_id, lang_code)

    def delete(self, indicator_id, lang_code):
        '''
        Method that deletes the country by its given code calling the dao
        '''
        self.tm.execute(self.dao, self.dao.delete, indicator_id, lang_code)

    def delete_all(self):
        '''
        Method that deletes all countries by calling the dao
        @attention: Take care of what you do, all countries will be destroyed
        '''
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.indicator_id, object.lang_code)


class TopicTranslationService(GenericService):
    """
    Service for region translation dao
    """

    def __init__(self):
        super(TopicTranslationService, self).__init__()
        self.dao = TopicTranslationDAO()

    def get_by_codes(self, topic_id, lang_code):
        '''
        Method that returns country given by the dao
        '''
        return self.tm.execute(self.dao, self.dao.get_by_codes, topic_id, lang_code)

    def delete(self, topic_id, lang_code):
        '''
        Method that deletes the country by its given code calling the dao
        '''
        self.tm.execute(self.dao, self.dao.delete, topic_id, lang_code)

    def delete_all(self):
        '''
        Method that deletes all countries by calling the dao
        @attention: Take care of what you do, all countries will be destroyed
        '''
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.topic_id, object.lang_code)


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



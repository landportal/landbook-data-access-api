"""
Created on 03/02/2014

:author: Weso
"""
from app import db
from app.daos import AuthDAO
from daos import DAO, CountryDAO, RegionTranslationDAO, IndicatorTranslationDAO, TopicTranslationDAO, RegionDAO
from model.models import Indicator, User, Organization, Observation, Region, DataSource, Dataset, Value, Topic, \
    IndicatorRelationship, MeasurementUnit


class GenericService(object):
    """
    Generic Service, it provides all default methods that could be used
    with the majority of the daos
    """

    def __init__(self):
        """
        Constructor for generic service
        """
        self.tm = TransactionManager()

    def get_all(self):
        """
        Method that returns all elements given by the dao
        :return: collection of elements
        """
        return self.tm.execute(self.dao, self.dao.get_all)

    def get_by_code(self, code):
        """
        Method that returns element given by the dao
        :param code: usually the id
        :return: element that owns the given id
        """
        return self.tm.execute(self.dao, self.dao.get_by_code, code)

    def insert(self, object):
        """
        Method that inserts a element calling the dao
        :param object: element to be persisted
        """
        self.tm.execute(self.dao, self.dao.insert, object)

    def delete(self, code):
        """
        Method that deletes the element by its given code calling the dao
        :param code: id of the element to be deleted
        """
        self.tm.execute(self.dao, self.dao.delete, code)

    def update(self, object):
        """
        Method that updates the element by calling the dao
        :param object: element to be updated with updated attributes
        """
        self.tm.execute(self.dao, self.dao.update, object)

    def delete_all(self):
        """
        Method that deletes all elements by calling the dao
        :attention: Take care of what you do, all countries will be destroyed
        """
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.id)

    def update_all(self, objects):
        """
        Method that updates all the elements given by calling the dao
        :params objects: list of objects to be updated with updated attributes
        """
        for object in objects:
            self.tm.execute(self.dao, self.dao.update, object)


class CountryService(GenericService):
    """
    Service for country dao
    """

    def __init__(self):
        """
        Constructor for country service
        """
        super(CountryService, self).__init__()
        self.dao = CountryDAO()

    def delete_all(self):
        """
        Method that deletes all countries by calling the dao
        :attention: Take care of what you do, all countries will be destroyed
        """
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.iso3)


class IndicatorService(GenericService):
    """
    Service for indicator dao
    """
    def __init__(self):
        """
        Constructor for indicator service
        """
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
        Constructor for organization service
        """
        super(ObservationService, self).__init__()
        self.dao = DAO(Observation)


class RegionService(GenericService):
    """
    Service for region dao
    """
    def __init__(self):
        """
        Constructor for region service
        """
        super(RegionService, self).__init__()
        self.dao = RegionDAO()

    def get_by_artificial_code(self, code):
        return self.tm.execute(self.dao, self.dao.get_by_artificial_code, code)

    def delete_all(self):
        """
        Method that deletes all regions by calling the dao
        :attention: Take care of what you do, all regions will be destroyed
        """
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.un_code)


class DataSourceService(GenericService):
    """
    Service for DataSource dao
    """
    def __init__(self):
        """
        Constructor for datasource service
        """
        super(DataSourceService, self).__init__()
        self.dao = DAO(DataSource)


class DatasetService(GenericService):
    """
    Service for Dataset dao
    """
    def __init__(self):
        """
        Constructor for dataset service
        """
        super(DatasetService, self).__init__()
        self.dao = DAO(Dataset)

    def insert(self, dataset):
        """
        Method that inserts a dataset calling the dao
        :param dataset: dataset to be persisted
        """
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
        """
        Constructor for value service
        """
        super(ValueService, self).__init__()
        self.dao = DAO(Value)


class TopicService(GenericService):
    """
    Service for Topic dao
    """
    def __init__(self):
        """
        Constructor for topic service
        """
        super(TopicService, self).__init__()
        self.dao = DAO(Topic)


class MeasurementUnitService(GenericService):
    """
    Service for measurement unit dao
    """
    def __init__(self):
        """
        Constructor for measurement unit service
        """
        super(MeasurementUnitService, self).__init__()
        self.dao = DAO(MeasurementUnit)


class IndicatorRelationshipService(GenericService):
    """
    Service for IsPartOf dao
    """
    def __init__(self):
        """
        Constructor for indicator relationship service
        """
        super(IndicatorRelationshipService, self).__init__()
        self.dao = DAO(IndicatorRelationship)


class RegionTranslationService(GenericService):
    """
    Service for region translation dao
    """
    def __init__(self):
        """
        Constructor for region translation service
        """
        super(RegionTranslationService, self).__init__()
        self.dao = RegionTranslationDAO()

    def get_by_codes(self, region_id, lang_code):
        """
        Method that returns translated region given by the dao
        :param region_id: id of requested region
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        :return: region translation
        """
        return self.tm.execute(self.dao, self.dao.get_by_codes, region_id, lang_code)

    def delete(self, region_id, lang_code):
        """
        Method that deletes the region translation by its given code calling the dao
        :param region_id: id of requested region
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        """
        self.tm.execute(self.dao, self.dao.delete, region_id, lang_code)

    def delete_all(self):
        """
        Method that deletes all region translation by calling the dao
        :attention: Take care of what you do, all countries will be destroyed
        """
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.region_id, object.lang_code)


class IndicatorTranslationService(GenericService):
    """
    Service for indicator translation dao
    """
    def __init__(self):
        """
        Constructor for indicator translation
        """
        super(IndicatorTranslationService, self).__init__()
        self.dao = IndicatorTranslationDAO()

    def get_by_codes(self, indicator_id, lang_code):
        """
        Method that returns translated indicator given by the dao
        :param indicator_id: id of requested indicator
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        :return: indicator translation
        """
        return self.tm.execute(self.dao, self.dao.get_by_codes, indicator_id, lang_code)

    def delete(self, indicator_id, lang_code):
        """
        Method that deletes the indicator translation by its given code calling the dao
        :param indicator_id: id of requested indicator
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        """
        self.tm.execute(self.dao, self.dao.delete, indicator_id, lang_code)

    def delete_all(self):
        """
        Method that deletes all indicator translations by calling the dao
        :attention: Take care of what you do, all countries will be destroyed
        """
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.indicator_id, object.lang_code)


class TopicTranslationService(GenericService):
    """
    Service for topic translation dao
    """
    def __init__(self):
        """
        Constructor for topic translation service
        """
        super(TopicTranslationService, self).__init__()
        self.dao = TopicTranslationDAO()

    def get_by_codes(self, topic_id, lang_code):
        """
        Method that returns translated topic given by the dao
        :param topic_id: id of requested topic
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        :return: topic translation
        """
        return self.tm.execute(self.dao, self.dao.get_by_codes, topic_id, lang_code)

    def delete(self, topic_id, lang_code):
        """
        Method that deletes the topic translation by its given code calling the dao
        :param topic_id: id of requested indicator
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        """
        self.tm.execute(self.dao, self.dao.delete, topic_id, lang_code)

    def delete_all(self):
        """
        Method that deletes all countries by calling the dao
        :attention: Take care of what you do, all topic translations will be destroyed
        """
        objects = self.tm.execute(self.dao, self.dao.get_all)
        for object in objects:
            self.tm.execute(self.dao, self.dao.delete, object.topic_id, object.lang_code)


class AuthService(GenericService):
    """
    Service for auth user dao
    """
    def __init__(self):
        """
        Constructor for auth user service
        """
        super(AuthService, self).__init__()
        self.dao = AuthDAO()


class TransactionManager(object):
    """
    Transaction manager that helps to abstract from the execution
    """
    def execute(self, dao, function, *args):
        """
        Abstraction for all calls to the dao methods, like command executor
        """
        session = db.session
        getattr(dao, 'set_session')(session)
        result = function(*args)
        session.commit()
        return result



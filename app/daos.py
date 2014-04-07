'''
Created on 03/02/2014

@author: Herminio
'''
from model.models import Country, RegionTranslation, IndicatorTranslation, TopicTranslation, Indicator, Dataset, Region


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


class RegionDAO(DAO):
    def __init__(self):
        super(RegionDAO, self).__init__(Region)

    def get_by_code(self, code):
        '''
        Method that returns a country by its given code
        '''
        return self.session.query(self.cls).filter_by(un_code=code).first()

    def update(self, object):
        '''
        Method to update an existing country, its code will not be changed
        '''
        persisted_object = self.get_by_code(object.un_code)
        update_object_attributes(persisted_object, object)


class RegionTranslationDAO(DAO):
    def __init__(self):
        super(RegionTranslationDAO, self).__init__(RegionTranslation)

    def get_by_codes(self, region_id, lang_code):
        return self.session.query(self.cls).filter(RegionTranslation.region_id == region_id)\
            .filter(RegionTranslation.lang_code == lang_code).first()

    def delete(self, region_id, lang_code):
        '''
        Method to delete an existing item by its code
        '''
        object = self.get_by_codes(region_id, lang_code)
        self.session.delete(object)

    def update(self, object):
        '''
        Method to update an existing country, its code will not be changed
        '''
        persisted_object = self.get_by_codes(object.region_id, object.lang_code)
        update_object_attributes(persisted_object, object)


class IndicatorTranslationDAO(DAO):
    def __init__(self):
        super(IndicatorTranslationDAO, self).__init__(IndicatorTranslation)

    def get_by_codes(self, indicator_id, lang_code):
        return self.session.query(self.cls).filter(IndicatorTranslation.indicator_id == indicator_id)\
            .filter(IndicatorTranslation.lang_code == lang_code).first()

    def delete(self, indicator_id, lang_code):
        '''
        Method to delete an existing item by its code
        '''
        object = self.get_by_codes(indicator_id, lang_code)
        self.session.delete(object)

    def update(self, object):
        '''
        Method to update an existing country, its code will not be changed
        '''
        persisted_object = self.get_by_codes(object.indicator_id, object.lang_code)
        update_object_attributes(persisted_object, object)


class TopicTranslationDAO(DAO):
    def __init__(self):
        super(TopicTranslationDAO, self).__init__(TopicTranslation)

    def get_by_codes(self, topic_id, lang_code):
        return self.session.query(self.cls).filter(TopicTranslation.topic_id == topic_id)\
            .filter(TopicTranslation.lang_code == lang_code).first()

    def delete(self, topic_id, lang_code):
        '''
        Method to delete an existing item by its code
        '''
        object = self.get_by_codes(topic_id, lang_code)
        self.session.delete(object)

    def update(self, object):
        '''
        Method to update an existing country, its code will not be changed
        '''
        persisted_object = self.get_by_codes(object.topic_id, object.lang_code)
        update_object_attributes(persisted_object, object)


def update_object_attributes(persisted_object, object):
    for attr in dir(persisted_object):
            if hasattr(object, attr) and attr[0] is not "_":
                setattr(persisted_object, attr, getattr(object, attr))
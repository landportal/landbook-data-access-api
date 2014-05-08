"""
Created on 03/02/2014

:author: Herminio
"""

from model.models import Country, RegionTranslation, IndicatorTranslation, TopicTranslation, Region, Auth


class DAO(object):
    """
    Generic DAO for all classes, only the class is needed
    """
    def __init__(self, cls):
        """
        Constructor for DAO
        :param cls: class to use in the dao
        """
        self.cls = cls

    def set_session(self, session):
        """
        Method to set the database to use
        :param session: session of the database used
        """
        self.session = session
        
    def get_all(self):
        """
        Method that returns all countries in the database
        :return: a collection of all elements
        """
        return self.session.query(self.cls).all()

    def get_by_code(self, code):
        """
        Method that returns a element by its given code
        :param code: id of the element requested
        :return: element with the given id
        """
        return self.session.query(self.cls).filter_by(id=code).first()
    
    def insert(self, object):
        """
        Method that inserts a new element
        :param object: element to be inserted
        """
        self.session.add(object)
    
    def delete(self, code):
        """
        Method to delete an existing element by its code
        :param code: id of the object to be deleted
        """
        object = self.get_by_code(code)
        self.session.delete(object)

    def update(self, object):
        """
        Method to update an existing element, its code will not be changed
        :param object: object to be updated, with updated attributes
        """
        persisted_object = self.get_by_code(object.id)
        update_object_attributes(persisted_object, object)


class CountryDAO(DAO):
    """
    Dao for country entity
    """
    def __init__(self):
        """
        Constructor for country dao
        """
        super(CountryDAO, self).__init__(Country)

    def get_by_code(self, code):
        """
        Method that returns a country by its given code
        :param code: iso3 of the country requested
        :return: country with given iso3
        """
        return self.session.query(self.cls).filter_by(iso3=code).first()

    def update(self, country):
        """
        Method to update an existing country, its code will not be changed
        :param country: country to be updated, with updated attributes
        """
        persisted_object = self.get_by_code(country.iso3)
        update_object_attributes(persisted_object, country)


class RegionDAO(DAO):
    """
    Dao for region entity
    """
    def __init__(self):
        """
        Constructor for region dao
        """
        super(RegionDAO, self).__init__(Region)

    def get_by_code(self, code):
        """
        Method that returns a region by its given code
        :param code: un_code of the region
        :return: region with given un_code
        """
        return self.session.query(self.cls).filter_by(un_code=code).first()


    def get_by_artificial_code(self, code):
        """
        Method that returns a region by its given code
        :param code: id of the region
        :return: region with given id
        """
        return self.session.query(self.cls).filter_by(id=code).first()

    def update(self, region):
        """
        Method to update an existing country, its code will not be changed
        :param region: region to be updated, with updated attributes
        """
        persisted_object = self.get_by_code(region.un_code)
        update_object_attributes(persisted_object, region)


class RegionTranslationDAO(DAO):
    """
    Dao for region translation entity
    """
    def __init__(self):
        """
        Contructor for region translation dao
        """
        super(RegionTranslationDAO, self).__init__(RegionTranslation)

    def get_by_codes(self, region_id, lang_code):
        """
        Method that returns translated region
        :param region_id: id of requested region
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        :return: region translation
        """
        return self.session.query(self.cls).filter(RegionTranslation.region_id == region_id)\
            .filter(RegionTranslation.lang_code == lang_code).first()

    def delete(self, region_id, lang_code):
        """
        Method that deletes the region translation by its given code
        :param region_id: id of requested region
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        """
        region_translation = self.get_by_codes(region_id, lang_code)
        self.session.delete(region_translation)

    def update(self, region_translation):
        """
        Method to update an existing region translation, its code will not be changed
        :param region_translation: updated region translation, with updated attributes
        """
        persisted_object = self.get_by_codes(region_translation.region_id, region_translation.lang_code)
        update_object_attributes(persisted_object, region_translation)


class IndicatorTranslationDAO(DAO):
    """
    Dao for indicator translation entity
    """
    def __init__(self):
        """
        Constructor for indicator translation dao
        """
        super(IndicatorTranslationDAO, self).__init__(IndicatorTranslation)

    def get_by_codes(self, indicator_id, lang_code):
        """
        Method that returns translated indicator
        :param indicator_id: id of requested indicator
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        :return: indicator translation
        """
        return self.session.query(self.cls).filter(IndicatorTranslation.indicator_id == indicator_id)\
            .filter(IndicatorTranslation.lang_code == lang_code).first()

    def delete(self, indicator_id, lang_code):
        """
        Method that deletes the indicator translation by its given code
        :param indicator_id: id of requested indicator
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        """
        indicator_translation = self.get_by_codes(indicator_id, lang_code)
        self.session.delete(indicator_translation)

    def update(self, indicator_translation):
        """
        Method to update an existing indicator translation, its code will not be changed
        :param indicator_translation: updated indicator translation, with updated attributes
        """
        persisted_object = self.get_by_codes(indicator_translation.indicator_id, indicator_translation.lang_code)
        update_object_attributes(persisted_object, indicator_translation)


class TopicTranslationDAO(DAO):
    """
    Dao for topic translation entity
    """
    def __init__(self):
        """
        Constructor for topic translation dao
        """
        super(TopicTranslationDAO, self).__init__(TopicTranslation)

    def get_by_codes(self, topic_id, lang_code):
        """
        Method that returns translated topic
        :param topic_id: id of requested topic
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        :return: topic translation
        """
        return self.session.query(self.cls).filter(TopicTranslation.topic_id == topic_id)\
            .filter(TopicTranslation.lang_code == lang_code).first()

    def delete(self, topic_id, lang_code):
        """
        Method that deletes the topic translation by its given code calling the dao
        :param topic_id: id of requested indicator
        :param: lang_code: code of the language like: 'en', 'es', 'fr'
        """
        topic_translation = self.get_by_codes(topic_id, lang_code)
        self.session.delete(topic_translation)

    def update(self, topic_translation):
        """
        Method to update an existing country, its code will not be changed
        :param topic_translation: updated topic translation, with updated attributes
        """
        persisted_object = self.get_by_codes(topic_translation.topic_id, topic_translation.lang_code)
        update_object_attributes(persisted_object, topic_translation)


class AuthDAO(DAO):
    """
    Dao for auth user entity
    """
    def __init__(self):
        """
        Constructor for auth user dao
        """
        super(AuthDAO, self).__init__(Auth)

    def get_by_code(self, username):
        """
        Method that returns a country by its given code
        :param username: name of the username requested
        :return: user with given username
        """
        return self.session.query(self.cls).filter_by(user=username).first()

    def update(self, auth):
        """
        Method to update an existing auth user, its username will not be changed
        :param auth: user auth to be updated, with updated attributes
        """
        persisted_object = self.get_by_code(auth.user)
        update_object_attributes(persisted_object, auth)


def update_object_attributes(object_to_update, object_with_new_attributes):
    """
    Updates all the attributes of an object with other object values
    all attributes beginning with '_' will not be updated
    :param object_to_update: object to be updated
    :param object_with_new_attributes: object with the new values
    """
    for attr in dir(object_to_update):
            if hasattr(object_with_new_attributes, attr) and attr[0] is not "_":
                setattr(object_to_update, attr, getattr(object_with_new_attributes, attr))
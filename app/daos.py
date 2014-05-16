"""
Created on 03/02/2014

:author: Weso
"""

from model.models import Country, RegionTranslation, IndicatorTranslation, TopicTranslation, Region, Auth, Observation, \
    Value, Indicator, Dataset, DataSource
from sqlalchemy import desc, func


global_expression = ((Region.is_part_of_id == '2') | (Region.is_part_of_id == '3') | (Region.is_part_of_id == '4')
                | (Region.is_part_of_id == '5') | (Region.is_part_of_id == '6'))

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


class IndicatorDAO(DAO):
    """
    Dao for indicator entity
    """
    def __init__(self):
        """
        Constructor for indicator dao
        """
        super(IndicatorDAO, self).__init__(Indicator)

    def get_indicators_by_country(self, iso3):
        return self.session.query(Indicator).join(Observation).join(Country).filter(Country.iso3 == iso3).all()

    def get_indicator_by_country(self, iso3, indicator_id):
        return self.session.query(Indicator).join(Observation).join(Country).filter(Country.iso3 == iso3)\
            .filter(Indicator.id == indicator_id).first()

    def get_starred_indicators(self):
        return self.session.query(Indicator).filter(Indicator.starred == True).all()

    def get_average(self, indicator_id):
        return self.session.query(func.avg(Value.value)).join(Observation)\
            .filter(Observation.indicator_id == indicator_id).filter(Value.value != 'null').first()

    def get_indicators_by_datasource(self, datasource_id):
        return self.session.query(Indicator).join((Indicator, Dataset.indicators)).filter(Dataset.datasource_id == datasource_id).all()


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

    def get_by_id(self, code):
        """
        Method that returns a country by its given id
        :param code: id of the country requested
        :return: country with given id
        """
        return self.session.query(self.cls).filter_by(id=code).first()

    def update(self, country):
        """
        Method to update an existing country, its code will not be changed
        :param country: country to be updated, with updated attributes
        """
        persisted_object = self.get_by_code(country.iso3)
        update_object_attributes(persisted_object, country)

    def get_countries_by_region(self, id):
        if id == 1:
            return self.session.query(Country).filter(global_expression).all()
        else:
            return self.session.query(Country).filter(Country.is_part_of_id == id).all()

    def get_country_by_region(self, region_id, iso3):
        if region_id == 1:
            return self.session.query(Country).filter(global_expression)\
                .filter(Country.iso3 == iso3).first()
        else:
            return self.session.query(Country).filter(Country.is_part_of_id == region_id)\
                .filter(Country.iso3 == iso3).first()

    def get_countries_with_data_by_region(self, id):
        if id == 1:
            return self.session.query(Country).join(Observation).filter(global_expression).group_by(Country.id).all()
        else:
            return self.session.query(Country).join(Observation).filter(Country.is_part_of_id == id).group_by(Country.id).all()


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

    def get_all_regions(self):
        return self.session.query(self.cls).filter_by(type='regions').all()

    def get_regions_of_region(self, id):
        return self.session.query(Region).filter(Region.type == 'regions').filter(Region.is_part_of_id == id).all()

    def get_regions_with_data(self, indicator_id):
        regions_ids = self.session.query(Country).join(Observation).filter(Observation.indicator_id == indicator_id)\
            .group_by(Country.is_part_of_id).all()
        return [self.get_by_artificial_code(region_id.is_part_of_id) for region_id in regions_ids]

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


class ObservationDAO(DAO):
    def __init__(self):
        """
        Constructor for observation translation dao
        """
        super(ObservationDAO, self).__init__(Observation)

    def get_by_region_and_indicator(self, region_id, indicator_id):
        if region_id == 1:
            return self.session.query(Observation).join(Region).filter(Observation.indicator_id == indicator_id)\
                .filter(global_expression).all()
        else:
            return self.session.query(Observation).join(Region).filter(Observation.indicator_id == indicator_id)\
                .filter(Region.is_part_of_id == region_id).all()

    def get_by_country_and_indicator(self, indicator_id, iso3):
        return self.session.query(Observation).join(Country).filter(Observation.indicator_id == indicator_id)\
            .filter(Country.iso3 == iso3).all()

    def get_top_by_region(self, indicator_id, region_id, top):
        if region_id == 1:
            return self.session.query(Observation).join(Value).join(Region).filter(

                ).filter(Observation.indicator_id == indicator_id).order_by(desc(Observation.value)).limit(top).all()
        else:
            return self.session.query(Observation).join(Value).join(Region).filter(Region.is_part_of_id == region_id)\
                .filter(Observation.indicator_id == indicator_id).order_by(desc(Observation.value)).limit(top).all()

    def get_starred_observations_by_country(self, iso3):
        return self.session.query(Observation).join(Indicator).join(Country).filter(Country.iso3 == iso3)\
            .filter(Indicator.starred == True).all()

    def get_by_indicator(self, indicator_id):
        return self.session.query(Observation).join(Value).filter(Observation.indicator_id == indicator_id)\
            .filter(Value.value != 'null').all()


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
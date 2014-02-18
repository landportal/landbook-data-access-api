'''
Created on 03/02/2014

@author: Herminio
'''
from app import db
import sqlalchemy
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String, TIMESTAMP, BOOLEAN
from sqlalchemy.orm import relationship
from abc import abstractmethod

class User(db.Model):
    '''
    User model object
    '''
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    ip = Column(String(50))
    timestamp = Column(TIMESTAMP)
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    organization = relationship("Organization")


    def __init__(self, user_id = None, ip = None, timestamp = None, organization = None):
        '''
        Constructor for user model object
        '''
        self.user_id = user_id
        self.ip = ip
        self.timestamp = timestamp
        self.organization = organization

class Organization(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    url = Column(String(255))
    is_part_of_id = Column(Integer, ForeignKey('organizations.id'))
    is_part_of = relationship("organizations.id")
    datasources = relationship("Datasource")

    def __init__(self, name = None, url = None, is_part_of = None):
        '''
        Constructor
        '''
        self.name = name
        self.url = url
        self.is_part_of = is_part_of
        self.data_sources = []

    def add_data_source(self, data_source):
        self.data_sources.append(data_source)
        data_source.organization = self

class DataSource(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "datasources"
    source_id = Column(Integer, primary_key=True)
    name = Column(String(128))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    organization = relationship("Organization")
    datasets = relationship("Dataset")
    observations = relationship("Observation")

    def __init__(self, source_id = None, name = None, organization = None):
        '''
        Constructor
        '''
        self.source_id = source_id
        self.name = name
        self.organization = organization
        self.datasets = []
        self.observations = []

    def add_dataset(self, dataset):
        self.datasets.append(dataset)
        dataset.source = self

    def add_observation(self, observation):
        self.observations.append(observation)
        observation.provider = self


class Dataset(db.Model):
    '''
    classdocs
    '''
    __tablename__ = 'datasets'
    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer)
    name = Column(String(60))
    sdmx_frequency = Column(Integer)
    datasets = Column(Integer, ForeignKey("datasources.source_id"))
    slices = relationship("Slice")
    indicators = relationship("Indicator")
    observations = relationship("Observation")
    license_id = Column(Integer, ForeignKey("licenses.id"))
    license = relationship("License")

    def __init__(self, dataset_id = None, name = None, frequency = None, source = None):
        '''
        Constructor
        '''
        self.dataset_id = dataset_id
        self.name = name
        self.frequency = frequency
        self.source = source
        self.slices = []

    def add_slice(self, data_slice):
        self.slices.append(data_slice)
        data_slice.dataset = self

class Slice(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "slices"
    slice_id = Column(Integer, primary_key=True)
    indicator_id = Column(Integer, ForeignKey("indicators.id"))
    dimension_id = Column(Integer, ForeignKey("dimensions.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.dataset_id"))
    dataset = relationship("DataSet")
    indicator = relationship("Indicator")
    dimension = relationship("Dimension")

    def __init__(self, slice_id = None, dimension = None, dataset = None, indicator = None):
        '''
        Constructor
        '''
        self.dataset = dataset
        self.indicator = indicator
        self.slice_id = slice_id
        self.dimension = dimension
        self.observations = []

    def add_observation(self, observation):
        self.observations.append(observation)
        observation.data_slice = self

class Observation(db.Model):
    '''
    classdocs
    '''
    __tablename__= "observations"
    id = Column(Integer, primary_key=True)
    observation_id = Column(Integer)
    ref_time_id = Column(Integer, ForeignKey("times.id"))
    issued_id = Column(Integer, ForeignKey("instants.id"))
    computation_id = Column(Integer, ForeignKey("computations.id"))
    indicator_group_id = Column(Integer, ForeignKey("indicatorGroups.id"))
    value_id = Column(Integer, ForeignKey("values.id"))
    indicator_id = Column(Integer, ForeignKey("indicators.id"))
    region_id = Column(Integer, ForeignKey("regions.id"))
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    dataset = relationship("Dataset")
    ref_time = relationship("Time")
    issued = relationship("Instant")
    computation = relationship("Computation")
    value = relationship("Value")
    indicator = relationship("Indicator")
    indicator_group = relationship("IndicatorGroup")
    region = relationship("Region")


    def __init__(self, observation_id = None, ref_time = None, issued = None,
                 computation = None, value = None, indicator = None, provider = None):
        '''
        Constructor
        '''
        self.observation_id = observation_id
        self.ref_time = ref_time
        self.issued = issued
        self.computation = computation
        self.value = value
        self.indicator = indicator
        self.provider = provider


class Indicator(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "indicators"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    measurement_unit_id = Column(String(20), ForeignKey("measurementUnits.name"))
    measurement_unit = relationship("MeasurementUnit")
    dataset_id = Column(Integer, ForeignKey("datasets.id"))
    dataset = relationship("Dataset")
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'indicators',
        'polymorphic_on': type
    }

    def __init__(self, name = None, description = None,
                 license_type = None, measurement_unit = None):
        '''
        Constructor
        '''
        self.name = name
        self.id = "http://landportal.info/ontology/indicator/" + name
        self.description = description
        self.license_type = license_type
        self.measurement_unit = measurement_unit

class IndicatorGroup(Indicator):
    '''
    classdocs
    '''
    __tablename__ = "indicatorGroups"
    id = Column(Integer, ForeignKey("indicators.id"), primary_key=True)
    observations = relationship("Observation")

    __mapper_args__ = {
        'polymorphic_identity': 'indicatorGroups',
    }


class MeasurementUnit(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "measurementUnits"
    name = Column(String(20), primary_key=True)

    def __init__(self, name = None):
        '''
        Constructor
        '''
        self.name = name

class License(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    republish = Column(BOOLEAN)
    url = Column(String(128))

    def __init__(self, name = None, description = None, republish = None, url = None):
        '''
        Constructor
        '''
        self.name = name
        self.description = description
        self.republish = republish
        self.url = url

class Computation(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "computations"
    id = Column(Integer, primary_key=True)
    uri = Column(String(60))

    def __init__(self, uri = None):
        '''
        Constructor
        '''
        self.uri = uri

class Value(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "values"
    id = Column(Integer, primary_key=True)
    obs_status = Column(String(50))
    value_type = Column(String(50))
    value = Column(String(50))

    def __init__(self, obs_status = None):
        '''
        Constructor
        '''
        self.obs_status = obs_status


class IndicatorRelationship(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "indicatorRelationships"
    id = Column(Integer, primary_key=True)
    source = Column(Integer, ForeignKey("indicators.id"))
    target = Column(Integer, ForeignKey("indicators.id"))
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'indicatorRelationships',
        'polymorphic_on': type
    }

    def __init__(self, source = None, target = None):
        '''
        Constructor
        '''
        self.source = source
        self.target = target

class IsPartOf(IndicatorRelationship):
    '''
    classdocs
    '''
    __tablename__ = "ispartof"
    id = Column(Integer, ForeignKey("indicatorRelationships.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'ispartof',
    }


    def __init__(self, source = None, target = None):
        '''
        Constructor
        '''
        super(IsPartOf, self).__init__(source, target)


class Becomes(IndicatorRelationship):
    '''
    classdocs
    '''
    __tablename__ = "becomes"
    id = Column(Integer, ForeignKey("indicatorRelationships.id"), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'becomes',
    }

    def __init__(self, source = None, target = None):
        '''
        Constructor
        '''
        super(Becomes, self).__init__(source, target)

class Dimension(db.Model):
    '''
    classdocs
    '''
    __tablename__ = "dimensions"
    id = Column(Integer, primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity':'dimensions',
        'polymorphic_on':type
    }

    @abstractmethod
    def get_dimension_string(self): pass

class Time(Dimension):
    '''
    classdocs
    '''
    __tablename__ = "times"
    id = Column(Integer, ForeignKey("dimensions.id"), primary_key=True)
    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'times',
    }

    @abstractmethod
    def get_time_string(self): pass

    def get_dimension_string(self):
        return self.get_time_string()


class Instant(Time):
    '''
    classdocs
    '''
    __tablename__ = "instants"
    id = Column(Integer, ForeignKey("times.id"), primary_key=True)
    timestamp = Column(TIMESTAMP)

    __mapper_args__ = {
        'polymorphic_identity':'instants',
    }

    def __init__(self, instant = None):
        '''
        Constructor
        '''
        self.instant = instant

    def get_time_string(self):
        return self.instant.strftime("%Y-%m-%dT%H:%M:%S")

class Interval(Time):
    '''
    classdocs
    '''
    __tablename__ = "intervals"
    id = Column(Integer, ForeignKey("times.id"), primary_key=True)
    start_time = Column(sqlalchemy.Time)
    end_time = Column(sqlalchemy.Time)

    __mapper_args__ = {
        'polymorphic_identity':'intervals',
    }

    def __init__(self, start_time = None, end_time = None):
        '''
        Constructor
        '''
        self.start_time = start_time
        self.end_time = end_time

    def get_time_string(self):
        return str(self.start_time) + '-' + str(self.end_time)

class YearInterval(Interval):
    '''
    classdocs
    '''
    __tablename__ = "yearIntervals"
    id = Column(Integer, ForeignKey("intervals.id"), primary_key=True)
    year = Column(Integer)

    __mapper_args__ = {
        'polymorphic_identity':'yearIntervals',
    }

    def __init__(self, start_time = None, end_time = None, year = None):
        '''
        Constructor
        '''
        super(YearInterval, self).__init__(start_time, end_time)
        self.year = year

    def get_time_string(self):
        return str(self.year)

class Region(Dimension):
    '''
    classdocs
    '''
    __tablename__ = "regions"
    id = Column(Integer, ForeignKey("dimensions.id"), primary_key=True)
    name = Column(String(128))
    is_part_of_id = Column(Integer, ForeignKey("regions.id"))
    is_part_of = relationship("Region")
    observations = relationship("Observation")

    __mapper_args__ = {
        'polymorphic_identity': 'regions',
    }

    def __init__(self, name = None, is_part_of = None):
        '''
        Constructor
        '''
        self.name = name
        self.is_part_of = is_part_of
        self.observations = []

    def add_observation(self, observation):
        self.observations.append(observation)
        observation.region = self

    def get_dimension_string(self):
        return self.name

class Country(Region):
    '''
    classdocs
    '''
    __tablename__ = "countries"
    id = Column(Integer, ForeignKey("regions.id"), primary_key=True)
    iso2 = Column(String(10))
    iso3 = Column(String(10))

    __mapper_args__ = {
        'polymorphic_identity': 'countries',
    }

    def __init__(self, name = None, is_part_of = None, iso2 = None, iso3 = None):
        '''
        Constructor
        '''
        super(Country, self).__init__(name, is_part_of)
        self.iso2 = iso2
        self.iso3 = iso3

    def get_dimension_string(self):
        return self.iso3



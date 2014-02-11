'''
Created on 03/02/2014

@author: Herminio
'''
from app import db
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

class Country(db.Model):
    '''
    Country model object
    '''   
    __tablename__ = 'countries'
    
    idCountry = Column(Integer, primary_key=True)
    idRegion = Column(Integer)
    faoURI = Column(String)
    iso_code2 = Column(String)
    iso_code3 = Column(String)
    

    def __init__(self, idRegion, faoURI, iso_code2, iso_code3):
        '''
        Constructor for country model object
        '''
        self.idRegion = idRegion
        self.faoURI = faoURI
        self.iso_code2 = iso_code2
        self.iso_code3 = iso_code3




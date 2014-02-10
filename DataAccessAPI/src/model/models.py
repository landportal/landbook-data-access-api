'''
Created on 03/02/2014

@author: Herminio
'''

class Country(object):
    '''
    Country model object
    '''

    def __init__(self, name, fao_URI, iso_code2, iso_code3):
        '''
        Constructor for country model object
        '''
        self.name = name
        self.fao_URI = fao_URI
        self.iso_code2 = iso_code2
        self.iso_code3 = iso_code3
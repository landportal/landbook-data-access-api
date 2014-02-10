'''
Created on 03/02/2014

@author: Herminio
'''
from src.model.models import Country


class CountryDAO(object):
    '''
    Country DAO
    '''
    SELECT_ALL_COUNTRIES_SQL = "SELECT * FROM Country;"
    SELECT_COUNTRY_BY_CODE_SQL = "SELECT * FROM Country WHERE isoCode3 = ?;"
    INSERT_COUNTRY_SQL = "INSERT INTO Country VALUES(?, ?, ?, ?);"
    DELETE_COUNTRY_SQL = "DELETE FROM Country WHERE isoCode3 = ?;"
    UPDATE_COUNTRY_SQL = "UPDATE Country SET isoCode2=?, faoURI=?, name=? WHERE isoCode3 = ?;"
    DELETE_ALL_COUNTRY_SQL = "DELETE FROM Country;"

    def set_database(self, db):
        '''
        Method to set the database to use
        '''
        self.db = db
        
    def get_all_countries(self):
        '''
        Method that returns all countries in the database
        '''
        country_list = []
        c = self.db.cursor()
        c.execute(self.SELECT_ALL_COUNTRIES_SQL)
        for row in c.fetchall():
            country_list.append(Country(row[3], row[0], row[1], row[2])) #this may change depending on the table implementation
        c.close()
        return country_list
    
    def get_country_by_code(self, code):
        '''
        Method that returns a country by its given code
        '''
        c = self.db.cursor()
        c.execute(self.SELECT_COUNTRY_BY_CODE_SQL, (code,))
        row = c.fetchone()
        country = None
        if row is not None:
            country = Country(row[3], row[0], row[1], row[2]) #this may change depending on the table implementation
        c.close()
        return country
    
    def insert_country(self, country):
        '''
        Method that inserts a new country
        '''
        c = self.db.cursor()
        c.execute(self.INSERT_COUNTRY_SQL, (country.fao_URI, country.iso_code2, 
                                            country.iso_code3, country.name)) #this may change depending on the table implementation
        c.close()
    
    def delete_country(self, code):
        '''
        Method to delete an existing country by its code
        '''
        c = self.db.cursor()
        c.execute(self.DELETE_COUNTRY_SQL, (code,))
        c.close()
        
    def update_country(self, country):
        '''
        Method to update an existing country, its code will not be changed
        '''
        c = self.db.cursor()
        print country.fao_URI
        c.execute(self.UPDATE_COUNTRY_SQL, (country.iso_code2, country.fao_URI, country.name, country.iso_code3))
        c.close()

    def delete_all_countries(self):
        '''
        Method to delete all the existing countries in the db
        @attention: Take care of what you do, all countries will be destroyed
        '''
        c = self.db.cursor()
        c.execute(self.DELETE_COUNTRY_SQL)
        c.close()
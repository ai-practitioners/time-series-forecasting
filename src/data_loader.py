from dotenv import dotenv_values
from logger import logging


class DBDataLoader():
    '''
        OOP-styled code for loading dataset from database.
        Since queries are read-only, we can use an alternative method
        to the one from Lesson 02 Notebook, which is easier to read.
    '''

    config = dotenv_values()
    logging.info("dotenv loaded into config successfully")


    def __init__(self):
        
        logging.info("[+] Local Connection Successful")
        
        self.query = 'SELECT * FROM full_df'


    def get_connection_string(self):

        USERNAME = self.config.get('USERNAME')
        PASSWORD = self.config.get('PASSWORD')
        ENDPOINT = self.config.get('ENDPOINT')
        DBNAME = self.config.get('DBNAME')

        return "mysql://"+USERNAME+":"+PASSWORD+"@"+ENDPOINT+":3306"+"/"+DBNAME

            


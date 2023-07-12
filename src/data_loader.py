from abc import ABC, abstractmethod
from dotenv import dotenv_values
from sqlalchemy import create_engine
import pandas as pd

from logger import logging

class DataLoader(ABC):
    '''
      Provide DataLoader interface for documentation purposes.
      Used for CSVDataLoader and DBDataLoader.
    '''
    @abstractmethod
    def load(self):
        pass


class CSVDataLoader(DataLoader):
    '''
      Implements load() method with pandas read_csv functionality
    '''
    def load(self, file_path="data/raw/stores.csv"):
        print('Loading CSV data...')
        return pd.read_csv(file_path)


class DBDataLoader(DataLoader):
    '''
        OOP-styled code for loading dataset from database.
        Since queries are read-only, we can use an alternative method
        to the one from Lesson 02 Notebook, which is easier to read.
    '''

    config = dotenv_values()
    logging.info("dotenv loaded into config successfully")


    def __init__(self):
        self.database = self._get_database_engine()
        logging.info("[+] Local Connection Successful")
        self.query = 'SELECT * FROM stores'


    def load(self, query=None):
        # If custom SQL query not provided, use default query
        if query is None:
            query = self.query
        print('Loading dataset from database...')
        
        return pd.read_sql(query, self.database, parse_dates='date', chunksize=10000)
    # (query, self.database, index_col='date', parse_dates='date', chunksize=10000)


    def _get_database_engine(self):
        host = self.config.get('ENDPOINT')
        port = int(self.config.get('PORT'))
        user = self.config.get('USERNAME')
        password = self.config.get('PASSWORD')
        db = self.config.get('DBNAME')

        return create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db}')

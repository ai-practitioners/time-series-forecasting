from sqlalchemy import create_engine
from abc import ABC, abstractmethod
from dotenv import dotenv_values
import polars as pl
import pandas as pd
import connectorx as cx
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
        return pl.read_csv(file_path)


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
        
        self.query = 'SELECT * FROM quito'


    def load(self, query=None):
        # If custom SQL query not provided, use default query
        if query is None:
            query = self.query
        print('Loading dataset from database...')
        
        # using connectorx
        return cx.read_sql(self.database, self.query )  
        # pd.read_sql(query, self.database, parse_dates='date', chunksize=10000)
        # pl.read_database(query=query, connection_uri=self.connection_uri)
        # pd.read_sql(query, self.database, parse_dates='date', chunksize=10000)


    def _get_database_engine(self):

        # local DB
        # port = int(self.config.get('PORT'))
        user = self.config.get('USERNAME')
        password = self.config.get('PASSWORD')
        host = self.config.get('ENDPOINT')
        db = self.config.get('DBNAME')
        
        # using connectorx
        # return f'mysql://mysql+mysqldb://{user}:{password}@{host}/{db}'
        # "mysql://{user}:{pw}@{host}:{port}/{db}".format(user=DB_USERNAME,
                                                    #    pw=DB_PASSWORD,
                                                    #    host=DB_HOST,
                                                    #    db=DB_DATABASE,
                                                    #    port=3306,
                                                    #    ssl_verify_identity=True,
                                                    #    ssl_ca="path/to/ssl_cert"
                                                    #    )
        # using mysql.connector
        # return mysql.connector.connect(f'mysql+mysqldb://{user}:{password}@{host}/{db}')
        # using sqlalchemy
        return create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')

    def get_connection_string(self, env, library):
        if env == "local":
            
            USERNAME = self.config.get('USERNAME')
            PASSWORD = self.config.get('PASSWORD')
            ENDPOINT = self.config.get('ENDPOINT')
            DBNAME = self.config.get('DBNAME')

            if library == "connectorx":
                return "mysql://"+USERNAME+":"+PASSWORD+"@"+ENDPOINT+":3306"+"/"+DBNAME
                # "mysql://"+{user}+":"+{password}+"@"+{host}:3306+"/"+{db}"
            elif library == "sqlalchemy":
                return "mysql+mysqlconnector://"+USERNAME+":"+PASSWORD+"@"+ENDPOINT+":3306"+"/"+DBNAME
            
        elif env == "remote":

            PS_USERNAME = self.config.get('PS_USERNAME')
            PS_PASSWORD = self.config.get('PS_PASSWORD')
            PS_HOST = self.config.get('PS_HOST')
            PS_DATABASE = self.config.get('PS_DATABASE')

            if library == "connectorx":
                return "mysql://"+PS_USERNAME+":"+PS_PASSWORD+"@"+PS_HOST+":3306"+"/"+PS_DATABASE
            elif library == "sqlalchemy":
                return "mysql+mysqlconnector://"+PS_USERNAME+":"+PS_PASSWORD+"@"+PS_HOST+":3306"+"/"+PS_DATABASE
        else:
            return None

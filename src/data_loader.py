from abc import ABC, abstractmethod
from dotenv import dotenv_values
import polars as pl
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
import MySQLdb
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
        
        self.query = 'SELECT * FROM quito_frm_view'


        # self.connection_uri=f'mysql+pymysql://{user}:{password}@{host}/{db}'
        # self.connection_uri=f'mysql+mysqldb://{user}:{password}@{host}/{db}'
        


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

        # planetscale
        # user = self.config.get("ps_username")
        # password = self.config.get("ps_password")
        # host = self.config.get("ps_host")
        # db = self.config.get("ps_database")
        
        # using connectorx
        return f'mysql://mysql+mysqldb://{user}:{password}@{host}/{db}'
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
        # return create_engine(f'mysql+mysqldb://{user}:{password}@{host}/{db}')

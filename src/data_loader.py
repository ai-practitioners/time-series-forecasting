import pymysql
import pandas as pd
from dotenv import load_dotenv
import os
from src.logger import logging

class DataLoader():
    '''
    For loading of dataset from local MySQL DB into the working environment
    '''
    def __init__(self):
        # load environment variables from .env
        load_dotenv()
        
        # extract db secrets
        self._host = os.getenv('ENDPOINT')
        self._port = int(os.getenv('PORT'))
        self._user = os.getenv('USERNAME')
        self._passwd = os.getenv('PASSWORD')
        self._dbname = os.getenv('DBNAME')
        
        # define type of cursor
        self._cursorclass = pymysql.cursors.DictCursor
        
    def initiate_local_connection(self):
        '''
        method that creates a connection to the db
        '''
        try:
            connection = pymysql.connect(
                host=self._host,
                port=self._port,
                user=self._user,
                passwd=self._passwd,
                db=self._dbname,
                cursorclass=self._cursorclass
            )
            
            print('[+] Local Connection Successful')
            logging.info("[+] Local Connection Successful")
            
        except Exception as e:
            print(f'[+] Local Connection Failed: {e}')
            logging.error(f'Error encountered: {e}', exc_info=True)
            connection = None

        return connection
    
    def query_from_string(self, connection, query):
        '''
        method that takes in a string as query, executes the query and return results as pandas DataFrame object
        '''
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                
            # Connection is not autocommit by default, so we must commit to save changes
            connection.commit()
            
            # Fetch all the records from SQL query output
            results = cursor.fetchall()
            
            # Convert results into pandas dataframe
            df = pd.DataFrame(results)
            
            print(f'Successfully retrieved records')
            logging.info("Successfully retrieved records")
            return df
    
        except Exception as e:
            print(f'Error encountered: {e}')
            logging.error(f'Error encountered: {e}', exc_info=True)
            
    def query_from_file(self, connection, file_path):
        '''
        method that accepts a .sql file, reads, execute the query within, and return results as pandas DataFrame object
        '''
        
        with open(file_path, 'r') as f:
            query = f.read()
            
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
            
            # Connection is not autocommit by default, so we must commit to save changes
            connection.commit()
            
            # Fetch all the records from SQL query output
            results = cursor.fetchall()
            
            # Convert results into pandas dataframe
            df = pd.DataFrame(results)
            
            print(f'Successfully retrieved records')
            logging.info("Successfully retrieved records")

            return df
        
        except Exception as e:
            print(f'Error encountered: {e}')
            logging.error(f'Error encountered: {e}', exc_info=True)

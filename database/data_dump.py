from src.configuration.mongodb_connection import MongoDBClient
from src.constant.database_details import DATABASE_NAME, DATA_DUMP_COLLECTION

import sys


from database_operations import Database_Operations



from src.logger import logging
from src.exceptions import CustomException
import os
import pandas as pd



class DataDump:
    
    def __init__(self,database_name = DATABASE_NAME,collection = DATA_DUMP_COLLECTION):
        self.raw_excel_data = 'data/Data_Train.xlsx'
        self.database_name = database_name
        self.collection_name = collection
        self.file_path = os.path.join('artifacts','retrieve_data.csv')
    



    def mongo_connection(self):
        try:
            client = MongoDBClient()
            if client is not None:
                return client.client
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def insert_raw_data(self):
        try:
            df = pd.read_excel(self.raw_excel_data)
            client = self.mongo_connection()
            data_ops = Database_Operations(client=client)
            data_ops.insert_pandas_dataframe(self.database_name,self.collection_name,df)
            


        except Exception as e:
            raise CustomException(e,sys)
        
    def get_data(self):
        try:

            client = self.mongo_connection()
            data_ops = Database_Operations(client=client)
            data_ops.retrieve_to_csv(self.database_name,self.collection_name,self.file_path)
            

        except Exception as e:
            raise CustomException(e,sys)
        







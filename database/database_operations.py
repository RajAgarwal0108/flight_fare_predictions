from src.exceptions import CustomException
from src.logger import logging

import pandas as pd
import sys



class Database_Operations:

    def __init__(self,client):
        self.client = client
        
        

    def insert_pandas_dataframe(self,database_name,collection_name,dataframe):

        try:
            db = self.client[database_name]
            collection = db[collection_name]
            dataframe.reset_index(inplace = True)
            data_dict = dataframe.to_dict("records")
            collection.insert_many(data_dict)
        except Exception as e:
            raise CustomException(e,sys)
        


    def retrieve_to_csv(self,database_name,collection_name,file_path):
        try:
            db = self.client[database_name]
            collection = db[collection_name]
            cursor = collection.find()
            cursor = pd.DataFrame(list(cursor))
            cursor = cursor[cursor.columns[1:]]
            cursor.to_csv(file_path)
            

        except Exception as e:
            raise CustomException(e,sys)
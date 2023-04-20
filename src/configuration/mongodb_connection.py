from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
from decouple import config


from src.constant.database_details import DATABASE_NAME
from src.logger import logging
from src.exceptions import CustomException






class MongoDBClient:
    logging.info("entered MongoClient...")

    client = None

    def __init__(self, database_name = DATABASE_NAME):
        try:
            if MongoDBClient.client is None:
                url = config('MONGODB_URL')

                if url is None:
                    raise CustomException('Environment key for mongoDB not set')
                
                MongoDBClient.client = MongoClient(url,server_api=ServerApi('1'))
            

            self.client = MongoDBClient.client

            self.database = self.client[database_name]

            self.database_name = database_name


        except Exception as e:
            raise CustomException(e,sys)
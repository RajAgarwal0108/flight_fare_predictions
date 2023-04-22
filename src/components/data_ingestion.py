from src.exceptions import CustomException
from src.logger import logging

import os
import sys
import pandas as pd
from dataclasses import dataclass

from sklearn.model_selection import train_test_split


@dataclass
class DataIngestionConfig:
    """
        Class Name : DataIngestionConfig
        Description : Data Class, defines the train and test file path 
    """
    logging.info("entered into DataIngestionConfig class")
    train_data_path: str = os.path.join("artifacts","train.csv")
    test_data_path: str = os.path.join("artifacts","test.csv")


class DataIngestion:

    """
        Class Name : DataIngestion
        Description : split dataset retrieve from database into train and test dataset
    """

    logging.info("enterd into DataIngestion Class")

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        """
            name : initaite_data_ingestion
            Description : Split data into train and test dataset
        """
        logging.log("data ingestion initated")

        try:
            df = pd.read_csv('artifacts/retrieve_data.csv')
            df.drop(columns=['Unnamed: 0','index'],inplace=True)

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)

            

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df,test_size=0.2,random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path,index = False,header=True)
            print('------------------------------------------------------------------------------------------------')
            print(train_set.head())

            test_set.to_csv(self.ingestion_config.test_data_path,index = False,header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
            

        except Exception as e:
            raise CustomException(e,sys)




import os
import sys

import numpy as np
import pandas as pd
import dill

from sklearn.metrics import r2_score
from src.logger import logging
from src.exceptions import CustomException

from sklearn.model_selection import GridSearchCV

def save_object(file_path,obj):
    logging.info("entered save_object in utils file")
    try:
        dir_path = os.path.dirname(file_path)

        logging.info("creating directory for saving object")

        os.makedirs(dir_path,exist_ok=True)

        logging.log('dumping object')

        with open(file_path, "wb") as file_obj:
            dill.dump(obj,file_obj)

        logging.info("object saved sucessfull!")
    except Exception as e:
        raise CustomException(e,sys)
    


def evaluate_models(X_train,y_train,X_test,y_test,models):

    logging.log("model ealuation started...")
    try:
        report = {}

        for i in range(len(list(models))):
            logging.info(f"evaluting model : {i} ")
         
            model = list(models.values())[i]
            

            model.fit(X_train,y_train)

          

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            logging.info("calculating model score")

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        
        logging.info("model evalution completed ... returning the report")
            
        return report
    
    except Exception as e:
        raise CustomException(e,sys)
    



def load_object(file_path):
    logging.info("entered load_object")

    try:
        logging.info("opening file to read...")

        with open(file_path,'rb') as file_obj:
            logging.info("reading file ... ... ...")
            file =  dill.load(file_obj)

        logging.info("file reading sucessfull ... \n returning the file")

        return file
        
        
    except Exception as e:
        raise CustomException(e,sys)
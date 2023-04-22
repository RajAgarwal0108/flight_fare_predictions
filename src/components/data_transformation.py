from src.exceptions import CustomException
from src.logger import logging

from src.components.preprocessing import Preprocessing
from src.components.preprocessing import scalerTransform

from sklearn.model_selection import train_test_split

import pandas as pd
import pickle
import numpy as np
import sys

class Data_Transformation:
    def __init__(self):
        pass
        

    def Initaite_Data_Transformation(self):
        try:
            data = pd.read_csv('artifacts/retrieve_data.csv')

            target_column = 'Price'

            input_feature = data.drop(columns=[target_column],axis=1)
            target_feature = data['Price']

            processed_data = Preprocessing(input_feature).process()

            print(processed_data.columns)
            processed_data.drop(columns=['Unnamed: 0','index'],axis=1,inplace=True)
            print(processed_data.columns)
        

            X_train,X_test,y_train,y_test = train_test_split(processed_data,target_feature,test_size=0.3,random_state=42)
            print("............................................")
            

            
            X_train_Scaled = scalerTransform().scaler(X_train)

            with open('artifacts/scaler.pickle','rb') as file:
                sc = pickle.load(file)

            X_test_Scaled = sc.transform(X_test)


            return(
                X_train_Scaled,
                X_test_Scaled,
                y_train,
                y_test
            )
            




        except Exception as e:
            raise CustomException(e,sys)
        


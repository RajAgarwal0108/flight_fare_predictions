import sys
import pandas as pd
from src.exceptions import CustomException
from src.logger import logging
from src.utils import load_object

from src.components.preprocessing import Preprocessing

class PredictPipeline:

    def __init__(self) -> None:
        pass


    def get_process(self,df):

        df = Preprocessing(df).process()
        fd = pd.read_csv('data/test_samp.csv')

        for i in fd.columns:
            df[i] = 0
        return df 

    def predict(self,features):

        try:
            model_path = 'artifacts/model.pkl'
            scaler_path = 'artifacts/scaler.pickle'
            model = load_object(file_path=model_path)
            print(model)
            scaler = load_object(file_path=scaler_path)

            fd = pd.DataFrame(features).T
            processed_data = self.get_process(fd)
            transformed_data = scaler.transform(processed_data)
            print(processed_data.columns)
            pred = model.predict(transformed_data)

            return  pred


        except Exception as e:
            raise CustomException(e,sys)
        


if __name__ == '__main__':
    ndf = pd.read_excel('data/Data_Train.xlsx')
    data = ndf.iloc[1]
    print(data)
    data.drop(['Price'],inplace=True)
    print(data)
    obj = PredictPipeline()
    print(obj.predict(data))

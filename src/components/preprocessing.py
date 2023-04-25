import pandas as pd
import os
import sys
import pickle
import datetime as dt

from sklearn.preprocessing import StandardScaler
from src.utils import save_object

from src.exceptions import CustomException
from src.logger import logging


class Preprocessing:
    
    logging.info("Entered Preprocessing class...")

    def __init__(self,dataframe):
        self.df = dataframe

    def process(self):

        logging.info("starting preprocessing of data ......")

        try:

            logging.info("processing Journey Date")

            self.df["Journey_day"]=pd.to_datetime(self.df["Date_of_Journey"],format="%d/%m/%Y").dt.day
            self.df["Journey_month"]=pd.to_datetime(self.df["Date_of_Journey"],format="%d/%m/%Y").dt.month

            self.df["Dep_hour"] = pd.to_datetime(self.df["Dep_Time"]).dt.hour
            self.df["Dep_min"] = pd.to_datetime(self.df["Dep_Time"]).dt.minute

            self.df["Arr_hour"] = pd.to_datetime(self.df["Arrival_Time"]).dt.hour
            self.df["Arr_min"] = pd.to_datetime(self.df["Arrival_Time"]).dt.minute

            logging.info("processing Journey Date completed")

            logging.info("processing Duration of flight")

            dur_hour=[]
            dur_min=[]
            for i in self.df.Duration:
                if 'h'in i and 'm' in i:
                    dur_hour.append(int(i.split('h')[0]))
                    dur_min.append(int(i.split('h')[1][:-1]))
                elif 'h' in i:
                    dur_hour.append(int(i.split('h')[0]))
                    dur_min.append(int(0))

                else:
                    dur_hour.append(int(0))
                    dur_min.append(int(i[:-1]))


            self.df['Duration_hour'] = dur_hour
            self.df['Duration_min'] = dur_min

            logging.info("processing Duration of flight completed")


            logging.info("dropping columns whioch are not required \n dropping ...")

            self.df.drop(columns=['Date_of_Journey','Route','Dep_Time','Arrival_Time','Duration','Additional_Info'],axis=1,inplace=True)

            logging.info('dropped!')

            logging.info('preparing columns and dataframe for further process...')

            self.df['Source'] = self.df.Source.apply(lambda x: "Source_" + x)
            self.df['Destination'] = self.df.Destination.apply(lambda x: "Destination_" + x)


            self.df['Total_Stops'] = self.df.Total_Stops.replace({"non-stop":0,"1 stop" : 1,"2 stops":2,"3 stops":3,"4 stops":4})

            self.df['Total_Stops'] = self.df.Total_Stops.fillna(self.df.Total_Stops.median())

            self.df['Total_Stops'] = self.df.Total_Stops.apply(lambda x: int(x))

            self.df = pd.concat([self.df,pd.get_dummies(self.df.Airline,drop_first=True)],axis=1)

            self.df = pd.concat([self.df,pd.get_dummies(self.df.Source,drop_first=True)],axis=1)

            self.df = pd.concat([self.df,pd.get_dummies(self.df.Destination,drop_first=True)],axis=1)

            self.df.drop(columns=['Airline','Source','Destination'],axis=1,inplace=True)

            logging.info("preprocessing completed successfully...!!!")


            

            return self.df

        
        

        except Exception as e:
            raise CustomException(e,sys)
        

class scalerTransform:

    logging.info("entered scalerTransform class ..")

    def __init__(self):

        logging.info("initializing scaler path..")

        self.scaler_path = os.path.join('artifacts','scaler.pickle')



    def scaler(self,X):

        try:

            logging.info("creating StandardScaler object and using fit transform on the dataset")

            sc = StandardScaler()

            x = sc.fit_transform(X)

            logging.info("saving scaler object")

            save_object(file_path=self.scaler_path,obj=sc)

            logging.info("Scaling task completed")

            return(x)



        except Exception as e:
            raise CustomException(e,sys)
        




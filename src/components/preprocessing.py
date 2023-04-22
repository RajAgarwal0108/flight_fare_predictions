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
    pass

    def __init__(self,dataframe):
        self.df = dataframe

    def process(self):

        try:

            self.df["Journey_day"]=pd.to_datetime(self.df["Date_of_Journey"],format="%d/%m/%Y").dt.day
            self.df["Journey_month"]=pd.to_datetime(self.df["Date_of_Journey"],format="%d/%m/%Y").dt.month

            self.df["Dep_hour"] = pd.to_datetime(self.df["Dep_Time"]).dt.hour
            self.df["Dep_min"] = pd.to_datetime(self.df["Dep_Time"]).dt.minute

            self.df["Arr_hour"] = pd.to_datetime(self.df["Arrival_Time"]).dt.hour
            self.df["Arr_min"] = pd.to_datetime(self.df["Arrival_Time"]).dt.minute

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

            self.df.drop(columns=['Date_of_Journey','Route','Dep_Time','Arrival_Time','Duration','Additional_Info'],axis=1,inplace=True)

            self.df['Source'] = self.df.Source.apply(lambda x: "Source_" + x)
            self.df['Destination'] = self.df.Destination.apply(lambda x: "Destination_" + x)


            self.df['Total_Stops'] = self.df.Total_Stops.replace({"non-stop":0,"1 stop" : 1,"2 stops":2,"3 stops":3,"4 stops":4})

            self.df['Total_Stops'] = self.df.Total_Stops.fillna(self.df.Total_Stops.median())

            self.df['Total_Stops'] = self.df.Total_Stops.apply(lambda x: int(x))

            self.df = pd.concat([self.df,pd.get_dummies(self.df.Airline,drop_first=True)],axis=1)

            self.df = pd.concat([self.df,pd.get_dummies(self.df.Source,drop_first=True)],axis=1)

            self.df = pd.concat([self.df,pd.get_dummies(self.df.Destination,drop_first=True)],axis=1)

            self.df.drop(columns=['Airline','Source','Destination'],axis=1,inplace=True)


            

            return self.df

        
        

        except Exception as e:
            raise CustomException(e,sys)
        

class scalerTransform:

    def __init__(self):
        self.scaler_path = os.path.join('artifacts','scaler.pickle')



    def scaler(self,X):

        try:
            sc = StandardScaler()
            x = sc.fit_transform(X)

            save_object(file_path=self.scaler_path,obj=sc)

            return(x)



        except Exception as e:
            raise CustomException(e,sys)
        




from flask import Flask, render_template, request
from src.pipeline.predict_pipeline import PredictPipeline
import pandas as pd
import numpy as np
import datetime as dt
import math

app = Flask(__name__)

 
airline_names = ['Air India','Air Asia', 'Spice Jet','Indigo','GoAir','Jet Airways','Jet Airways Business','Multiple carriers', 'Multiple carriers Premium economy','Trujet', 'Vistara', 'Vistara Premium economy']
sources = ['Banglore','Kolkata','Delhi','Chennai','Mumbai']
destination = ['New Delhi','Banglore','Cochin','Kolkata','Delhi','Hyerbad']
stops = ['non-stop','1 stop','2 stops','3 stops','4 stops']
@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index.html',airways=airline_names,source = sources,destination=destination,stops=stops)

@app.route('/predict',methods=['GET','POST'])
def predict():
    print('predicting...')
    print(request.method)
    if request.method == 'POST':
        airway= request.form.get('Airline')
        date = request.form.get('date')
        source = request.form.get('Source')
        destination = request.form.get('Destination')
        dep_time = request.form.get('dep_time')
        arr_time = request.form.get('arr_time')
        stops = request.form.get('Total_Stops')

        
   
        
        
        dl = date.split('-')
        date = dl[2]+'/'+dl[1]+'/'+dl[0]
        print(date)
        print(dep_time,',',arr_time)
        dur = f"{abs(int(arr_time.split(':')[0])- int(dep_time.split(':')[0]))}h {abs(int(arr_time.split(':')[1]) - int(dep_time.split(':')[1]))}m"
        print(dur) 
        data = {
            "Airline" : airway,
            "Date_of_Journey" : date,
            "Source" : sources,
            "Destination" : destination,
            "Route" : "route",
            "Dep_Time" : dep_time,
            "Arrival_Time" : arr_time,
            "Duration" : dur,
            "Total_Stops" : stops,
            "Additional_Info" : "info"
        }
        df = pd.DataFrame(data)
        pred = PredictPipeline().predict(df.iloc[0])
        print(pred)
        


        
        return render_template('predict.html',h1=math.ceil(pred[0]))
    else:
        return render_template('predict.html',h1='error')


if __name__ == '__main__':
    app.run(debug=True)
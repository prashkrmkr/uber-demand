import pandas as pd
import numpy as np
import sklearn
import sys
from datetime import datetime

from flask import Flask,request,jsonify,render_template

import joblib 

from sklearn.ensemble import RandomForestRegressor

model = joblib.load('model.joblib')

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['Post'])
def pred():
    
    datetime_raw = request.form.get('time')
    pickup_location = int(request.form.get('pickup_location_id'))
    trip_distnace = int(request.form.get('trip_distance'))

    date = datetime.fromisoformat(datetime_raw)

    hour = float(date.hour)
    day = float(date.day)
    month = float(date.month)
    weekday1 = date.weekday()
    def time_split(i):
        if 5<=i<12:
            return 0
        elif 12<=i<16:
            return 1
        elif 16<=i<20:
            return 2
        elif 20<=i<24:
            return 3
        elif i<5:
            return 4
    part_of_day = time_split(hour)
    weekends = 1 if weekday1==(5,6) else 0
    start_month = 1 if day==(1,2,3) else 0
    end_month = 1 if day==(28,29,30) else 0

    data = {'hour_pick':hour,'day_pick':day,'month_pick':month,'weekday_pick':weekday1,'PULocationID':pickup_location,
     'part_of_day':part_of_day,'weekends':weekends,'avg_distance':trip_distnace,'start_month':start_month,'end_month':end_month}

    feature = pd.DataFrame(data, index=[0])

    prediction = model.predict(feature)
    value = prediction*100/(28)
    output = f'the Demand is {'very high' if value>75 else 'high' if 75>value>50 else 'low' if 50>value>25 else 'very low' } & percentage is {value}'

    return render_template('index.html',prediction_text ='So according to given information {}'.format(output))

if __name__=='__main__':
    app.run(debug=True)



# d = {'hour_pick':12,'day_pick':15,'month_pick':5,'weekday_pick':5,'PULocationID':134,
#      'part_of_day':0,'weekends':0,'avg_distance':3.521,'start_month':0,'end_month':0}

# arr = pd.DataFrame(d,index=[0])

# print(pred(arr))

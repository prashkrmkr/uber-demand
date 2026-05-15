import pandas as pd
import numpy as np
import sklearn
import sys

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

    int_feat = [int(x) for x in request.form.values()]
    feature = [np.array(int_feat)]

    prediction = model.predict(feature)
    value = prediction*100/(28)
    output = f'The Demand is {'very high' if value>75 else 'high' if 75>value>50 else 'low' if 50>value>25 else 'very low' }'
    return render_template('index.html',prediction_text ='So:{}'.format(output))

if __name__=='__main__':
    app.run(debug=True)



# d = {'hour_pick':12,'day_pick':15,'month_pick':5,'weekday_pick':5,'PULocationID':134,
#      'part_of_day':0,'weekends':0,'avg_distance':3.521,'start_month':0,'end_month':0}

# arr = pd.DataFrame(d,index=[0])

# print(pred(arr))

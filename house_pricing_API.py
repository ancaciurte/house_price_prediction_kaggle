import pandas as pd
import numpy as np
import pickle5 as pickle
import datetime as dt
from time import time
from sklearn.preprocessing import LabelEncoder
import flask
from flask import request, jsonify, Flask
import json
from json_tricks import dumps
import sys


def preprocessing(df):
     #convert categorical to numerical
    lb = LabelEncoder()
    cat_variable = df.dtypes==object
    cat_variable = df.columns[cat_variable].tolist()
    df[cat_variable] = df[cat_variable].apply(lambda col: lb.fit_transform(col.astype(str)))

    return df   



#load the model from disk
lr = pickle.load(open('models/lr.sav', 'rb'))
knn = pickle.load(open('models/knn.sav', 'rb'))
svc = pickle.load(open('models/svc.sav', 'rb'))
tree = pickle.load(open('models/tree.sav', 'rb'))
forest = pickle.load(open('models/forest.sav', 'rb'))
gb = pickle.load(open('models/gb.sav', 'rb'))
xgb = pickle.load(open('models/xgb.sav', 'rb'))
lgbm = pickle.load(open('models/lgbm.sav', 'rb'))


app = Flask(__name__)

@app.route('/', methods=['POST'])
def predict():
    try:
        input_json = request.get_json()
        input_df =  preprocessing(pd.DataFrame(input_json))
    except Exception:
        print("Input exception: The received input is not in a valid json format!")
        return jsonify({})
   
  
    preds = pd.DataFrame(gb.predict(input_df), columns=[['Predicted Price']])
    return dumps(preds.to_json(orient="index")) #jsonify(preds) #

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=5320, threaded=True)



'''
input_json = [{ 
    'bathrooms': 2, 
    'floor': 0.5, 
    'rooms': 3, 
    'surface': 78, 
    'state': 'nou', 
    'zone': 'Buna Ziua'
},
{
    'bathrooms': 2, 
    'floor': 0.5, 
    'rooms': 3, 
    'surface': 78, 
    'state': 'renovat', 
    'zone': 'Marasti'
}]
'''
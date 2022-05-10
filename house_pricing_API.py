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


def preprocess_type(input_json):
    #convert categorical to numerical
    input_df = pd.DataFrame(input_json)
    lb = LabelEncoder()
    cat_variable = input_df.dtypes==object
    cat_variable = input_df.columns[cat_variable].tolist()
    input_df[cat_variable] = input_df[cat_variable].apply(lambda col: lb.fit_transform(col.astype(str)))
    return input_df


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
        input = request.get_json()
        input_df = preprocess_type(input)
    except Exception:
        print("Input exception: The received input is not in a valid json format!")
        return jsonify({})
   
  
    preds = pd.DataFrame(lr.predict(input_df), columns=[['Predicted Price']])
    return dumps(preds.to_json(orient="index")) #jsonify(preds) #

if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=5320, threaded=True)





'''
#input json example
[
    { 
        "bedrooms": 3,
        "bathrooms": 1.5,
        "sqft_living": 1340,
        "sqft_lot": 7912,
        "sqft_above":1340,
        "sqft_basement": 0,
        "floors": 1.5,
        "waterfront": 0,
        "view":0,
        "yr_built": 1955,
        "yr_renovated": 2005,
        "city": "Shoreline",
        "country": "USA",
        "renewal_status": 1
    },
    {
        "bedrooms": 3,
        "bathrooms": 1.5,
        "sqft_living": 1340,
        "sqft_lot": 7912,
        "sqft_above":1340,
        "sqft_basement": 0,
        "floors": 1.5,
        "waterfront": 0,
        "view":0,
        "yr_built": 1955,
        "yr_renovated": 2005,
        "city": "Shoreline",
        "country": "USA",
        "renewal_status": 1
    }
]

'''
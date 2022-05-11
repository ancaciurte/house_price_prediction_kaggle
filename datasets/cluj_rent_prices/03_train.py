# %%
import pandas as pd
import numpy as np

from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

if __name__ == '__main__':
    value_cols = [
        'surface', 'rooms', 'floor',
        'bathrooms'
    ]

    categ_cols = [
        'zone', 'state'
    ]

    target_cols = [
        'ad_price'
    ]

    file_path = 'data\processed\offers_cluj-napoca_2022-03-25.csv'

    df = pd.read_csv(file_path)

    df = df.loc[:, value_cols+categ_cols+target_cols].dropna()

    categ_enc = OrdinalEncoder()
    value_enc = StandardScaler()
    target_enc = StandardScaler()

    input_values = value_enc.fit_transform(df.loc[:, value_cols])
    input_categs = categ_enc.fit_transform(df.loc[:, categ_cols])
    
    X = np.concatenate([input_values, input_categs], axis=-1)
    y = target_enc.fit_transform(df.loc[:, target_cols])

    # Split the data into training/testing sets
    X_train = X[:-20]
    X_test = X[-20:]

    # Split the targets into training/testing sets
    y_train = y[:-20]
    y_test = y[-20:]

    # # Create linear regression object
    # regr = linear_model.LinearRegression()

    regr = MLPRegressor(hidden_layer_sizes=(256, 128, 64),
                        validation_fraction=0.3, learning_rate='adaptive',
                        random_state=1, max_iter=5000, early_stopping=True)

    # Train the model using the training sets
    regr.fit(X, y)

    # Make predictions using the testing set
    y_pred = regr.predict(X_test)

    # # The coefficients
    # print("Coefficients: \n", regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.2f" % r2_score(y_test, y_pred))

# %%
    data_Rares = {
        'surface': [50, 60, 60], 
        'rooms': [2, 2, 2], 
        'floor': [0.25, 0, 0.6],
        'bathrooms': [1, 1, 1],
        'zone': ['Zorilor', 'Zorilor', 'Gheorgheni'],
        'state': ['utilizat', 'utilizat', 'nou']
    }

    df = pd.DataFrame.from_dict(data_Rares)

    input_values = value_enc.transform(df.loc[:, value_cols])
    input_categs = categ_enc.transform(df.loc[:, categ_cols])
    
    X = np.concatenate([input_values, input_categs], axis=-1)
    
    y_pred = regr.predict(X)
    target_enc.inverse_transform(y_pred.reshape(-1, 1))
# %%

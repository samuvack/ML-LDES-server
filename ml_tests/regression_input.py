# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
import operator

bottle = pd.read_csv("data/bottle.csv")

# Extract 2 columns 'T_degC','Salnty' for pure and better showing
bottle_df = bottle[['T_degC','Salnty']]

# And called again
bottle_df.columns = ['Temperature', 'Salinity']

bottle_df = bottle_df[:][:500]      # lets take limit for speed regression calculating

bottle_df.isnull().sum()

# Drop NaN or missing input numbers
bottle_df.fillna(method='ffill', inplace=True)

# Features chose
X = np.array(bottle_df['Salinity']).reshape(-1, 1)
y = np.array(bottle_df['Temperature']).reshape(-1, 1)

# Split data as %20 is test and %80 is train set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 42)


def run_linear_model(x_input):
    # LINEAR REGRESSION
    from sklearn.linear_model import LinearRegression
    lin_df = LinearRegression()  
    lin_df.fit(X_train, y_train)
    y_pred = lin_df.predict([[x_input]])  
    return y_pred[0][0]


def run_random_forest(x_input):
    from sklearn.ensemble import RandomForestRegressor
    rf_reg = RandomForestRegressor(n_estimators=5, random_state=0)
    rf_reg.fit(X_train,y_train)
    rf_predict = rf_reg.predict([x_input])
    return rf_predict

def run_random_forest(x_input):
    from sklearn.ensemble import RandomForestRegressor
    rf_reg = RandomForestRegressor(n_estimators=5, random_state=0)
    rf_reg.fit(X_train,y_train)
    rf_predict = rf_reg.predict([x_input])
    return rf_predict

def run_multiple_lin_regression(x_input):
    # MULTIPLE LINEAR REGRESSION
    from sklearn.linear_model import LinearRegression
    mlin_df = LinearRegression()
    mlin_df = mlin_df.fit(X_train, y_train)
    mlin_df.intercept_       # constant b0
    mlin_df.coef_            # variable coefficient
    y_pred = mlin_df.predict([[x_input]])                                      # predict Multi linear Reg model
    return y_pred[0][0]


def run_polynomial_regression(x_input):
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    poly_df = PolynomialFeatures(degree = 4)
    transform_poly = poly_df.fit_transform(X_train)
    linreg2 = LinearRegression()
    linreg2.fit(transform_poly,y_train)
    polynomial_predict = linreg2.predict([[x_input]])
    return polynomial_predict

def run_decisiontreeregressor(x_input):
    # DECISION TREE REGRESSION
    from sklearn.tree import DecisionTreeRegressor
    dt_reg = DecisionTreeRegressor()
    dt_reg.fit(X_train,y_train)
    dt_predict = dt_reg.predict([[x_input]])
    return dt_predict[0]

print(run_linear_model(33))
print(run_decisiontreeregressor(33))
print(run_multiple_lin_regression(33))



import data_processing.get_dataframe_sensor
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
import pandas as pd
import offline_ml.prophet_output
import matplotlib.pyplot as plt

dat = data_processing.get_dataframe_sensor.get_df_sensor('urn:ngsi-v2:cot-imec-be:Device:dwg-iow-VvadXzCVFMBUK4WDEwfrkK')
print(dat)
dat.plot(x='time', y='conductivity', kind='line')
plt.show()
dat = dat.drop_duplicates(subset=['time'])

X = dat['time']
y = dat['conductivity']

tscv = TimeSeriesSplit(n_splits=5, test_size=60)
for train_index, test_index in tscv.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    train = pd.concat([X_train, y_train], axis=1)
    print('train')
    print(train)
    print(offline_ml.prophet_output.prophet_output(train, 'time', 'conductivity'))
    forecast = offline_ml.prophet_output.prophet_output(train, 'time', 'conductivity')
    #forecast.plot(x='ds', y = 'yhat', kind='line', color = 'red')  
    plt.scatter(forecast['ds'], forecast['yhat'], color='red')
    test = pd.concat([X_test, y_test], axis=1)
    print('TEST --------------------------------------------------------------')
    #print(test)
    plt.scatter(X_train,y_train, color='orange', s=0.1)
    plt.scatter(X_test, y_test, color='red', s=0.1)
    #print(test)
    plt.show()
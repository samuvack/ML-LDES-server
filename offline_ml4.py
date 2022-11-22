import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from psycopg2.extensions import AsIs
import psycopg2
import pandas.io.sql as sqlio
from sklearn.model_selection import TimeSeriesSplit
import matplotlib.pyplot as plt

hostname = 'localhost'
port='5432'
username = 'postgres'
password = 'password'
database = 'water_quality'

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database, port=port)
    print('connected')
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()
sql = "select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as time, temperatuur_value as temperature, conductiviteit_value as conductivity from public.water_quality where temperatuur_sensor = 'urn:ngsi-v2:cot-imec-be:Device:aqf-iow-JX3CPbvBck498C3uan9KNg' order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"
dat = sqlio.read_sql_query(sql, conn)
dat.insert(0, 'id', range(0, 0 + len(dat)))
print(dat)

X = dat['temperature'].to_numpy()
print(len(dat['temperature']))
y = np.arange(0, len(dat['temperature']))
print(y)

from sklearn.model_selection import TimeSeriesSplit
n_splits = 5
tscv = TimeSeriesSplit(n_splits)

for fold, (train_index, test_index) in enumerate(tscv.split(X)):
    #print("Fold: {}".format(fold))
    #print("TRAIN indices:", train_index, "\n", "TEST indices:", test_index)
    #print("\n")
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]



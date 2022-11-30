from psycopg2.extensions import AsIs
import psycopg2
from multiprocessing import Pool
import datetime
import multiprocessing
# arrays and dataframes
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd
import pandas.io.sql as sqlio
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
from river import datasets
from river import metrics
from river import time_series
from river import compose
from river import linear_model
from river import optim
from river import preprocessing

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


file_names = []



SQL = "select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as time, temperatuur_value as temperature, conductiviteit_value as conductivity from public.water_quality where temperatuur_sensor = 'urn:ngsi-v2:cot-imec-be:Device:aqf-iow-JX3CPbvBck498C3uan9KNg' order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"

dat = sqlio.read_sql_query(SQL, conn)

dat.insert(0, 'id', range(0, 0 + len(dat)))
print(dat)



sns.set()

fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)

dat.plot(x='time', y='temperature', kind='line', ax=axes[0], color='r')	

dat.plot(x='time', y='conductivity', kind='line', ax=axes[1])	
plt.tick_params(axis='x', rotation=90)
#plt.show()

conn = None



period = 1

global model
dataset = datasets.TrumpApproval()

model = linear_model.LogisticRegression()
metric = metrics.ROCAUC()

fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)


temperature_list = dat['temperature'].values.tolist()
conductivity_list = dat['conductivity'].values.tolist()
dataset = zip(conductivity_list, temperature_list)

print(temperature_list)

time_list = dat['id'].values.tolist()
print(time_list)


for x,y in dataset:
    y_pred = model.predict_proba_one(x)     
    model.learn_one(x, y)
    metric.update(y, y_pred)
    
    #Online Forecasting
    #forecast = model.forecast(horizon=12)
    #print(forecast)



import re
import time
from psycopg2.extensions import AsIs
import psycopg2
from multiprocessing import Pool
import datetime
import multiprocessing
# arrays and dataframes
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
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
import pickle
from varname import nameof

hostname = 'localhost'
port = '5432'
username = 'postgres'
password = 'password'
database = 'water_quality'

# Try to connect

try:
    conn = psycopg2.connect(host=hostname, user=username,
                            password=password, dbname=database, port=port)
    print('connected')
except:
    print("I am unable to connect to the database.")

cur = conn.cursor()


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def run_river_model(y, model):
    model = model.learn_one(y)
    forecast = model.forecast(horizon=12)
    print(forecast)
    sensor_name_new =  get_valid_filename(sensor_name)
    filename = 'river_model_'+  nameof(model) +'.sav'
    print(filename)
    pickle.dump(model, open(filename, 'wb'))

sensor_name = 'urn:ngsi-v2:cot-imec-be:Device:aqf-iow-JX3CPbvBck498C3uan9KNg'

sql = """select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp,
            temperatuur_value, conductiviteit_value from public.water_quality
            where temperatuur_sensor = '""" + sensor_name + """'
            order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"""

dat = sqlio.read_sql_query(sql, conn)

#dat.insert(0, 'id', range(0, 0 + len(dat)))
print(dat)

model1 = (
        time_series.SNARIMAX(
            p=1,
            d=0,
            q=0,
            m=1,
            sp=1,
            sq=6,
            regressor=(
                preprocessing.StandardScaler() |
                linear_model.LinearRegression(
                    intercept_init=110,
                    optimizer=optim.SGD(0.01),
                    intercept_lr=0.5
                )
            )
        )
    )

model2 = (
        time_series.SNARIMAX(
            p=1,
            d=0,
            q=0,
            m=1,
            sp=1,
            sq=6,
            regressor=(
                preprocessing.StandardScaler() |
                linear_model.LinearRegression(
                    intercept_init=110,
                    optimizer=optim.SGD(0.01),
                    intercept_lr=0.5
                )
            )
        )
    )


for row in dat.iterrows():
    print(row[1][1])
    
    run_river_model(row[1][1], model1, 'model1')
    
    run_river_model(row[1][1], model2, 'model2')



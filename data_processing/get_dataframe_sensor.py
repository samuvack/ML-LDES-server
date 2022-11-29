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
from sklearn.metrics import r2_score

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


def mae(y_true, predictions):
    """calculates Mean absolute error

    Args:
        y_true (list): true y values
        predictions (list): forecasted estimated y values

    Returns:
        float: _description_
    """
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))


def get_df_sensor(sensor_name):
    """get dataframe output of one sensor with unique id

    Args:
        sensor_name (text): unique id value of snesor

    Returns:
        _type_: _description_
    """
    sql = "select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as time, temperatuur_value as temperature, conductiviteit_value as conductivity,  ROW_NUMBER() OVER (ORDER BY id) as row from public.water_quality where temperatuur_sensor = '" + \
        sensor_name + \
        "' order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"
    print(sql)
    dat = sqlio.read_sql_query(sql, conn)
    dat.insert(0, 'id', range(0, 0 + len(dat)))
    
    return dat

print(get_df_sensor('urn:ngsi-v2:cot-imec-be:Device:dwg-iow-VvadXzCVFMBUK4WDEwfrkK'))
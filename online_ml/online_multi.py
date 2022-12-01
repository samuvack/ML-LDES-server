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



sql = "select replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp as time, temperatuur_value as temperature, conductiviteit_value as conductivity from public.water_quality where temperatuur_sensor = 'urn:ngsi-v2:cot-imec-be:Device:aqf-iow-JX3CPbvBck498C3uan9KNg' order by replace(Replace(temperatuur_date, 'T', ' '), 'Z', '')::timestamp"

dat = sqlio.read_sql_query(sql, conn)

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
model = (
time_series.SNARIMAX(
         p=1,
         d=0,
         q=1,
         m=1,
         sp=0,
         sq=0,
         sd=0,
         regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                optimizer=optim.SGD(0.05),
                intercept_lr=0.5
            )
     )
 )
)

model2 = (
time_series.SNARIMAX(
         p=1,
         d=0,
         q=1,
         m=1,
         sp=0,
         sq=0,
         sd=0,
         regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                intercept_init=110,
                optimizer=optim.SGD(0.01),
                intercept_lr=0.1
            )
     )
 )
)



model3 = (
time_series.SNARIMAX(
         p=4,
         d=4,
         q=12,
         m=7,
         sp=2,
         sq=3,
         sd=2,
         regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                optimizer=optim.SGD(0.01),
                intercept_lr=0.1
            )
     )
 )
)

def river_snarimax(p_input, m_input, sp_input, sgd_input, lr_input, model_name):
    model_name = (
    time_series.SNARIMAX(
    p=p_input,
    d=0,
    q=0,
    m=m_input,
    sp=sp_input,
    sq=6,
    regressor=(
        preprocessing.StandardScaler() |
        linear_model.LinearRegression(
            intercept_init=110,
            optimizer=optim.SGD(sgd_input),
            intercept_lr=lr_input
        )
    )
    )
    )


fig, axes = plt.subplots(nrows=2, ncols=1,sharex=True)


temperature_list = dat['temperature'].values.tolist()

print(temperature_list)

time_list = dat['id'].values.tolist()
print(time_list)


for i in range(len(dat)):
    print(i)
    print(dat.loc[i, "temperature"])
    model = model.learn_one(dat.loc[i, "temperature"])
    model2 = model2.learn_one(dat.loc[i, "temperature"])
    model3 = model3.learn_one(dat.loc[i, "temperature"])
    model4 = model4.learn_one(dat.loc[i, "temperature"])
    
    #Online Forecasting
    forecast = model.forecast(horizon=12)
    forecast2 = model2.forecast(horizon=12)
    forecast3 = model3.forecast(horizon=12)
    forecast4 = model.forecast(horizon=12)
    print(forecast)
    
    filename = 'finalized_model.sav'
    pickle.dump(model, open(filename, 'wb'))

    t_list2=[]
    temperature_filtered = []
    time_filtered=[]
    for j in range(12):
        t_list2.append(i+j+1)

    if i > 0:
        for t in range(24):
            temperature_filtered.append(temperature_list[i-12+t])
            time_filtered.append(time_list[i-12+t])
        print(temperature_filtered)
        print(time_filtered)
        #Plotting

        plt.figure()
        sns.set()
        plt.scatter(time_filtered, temperature_filtered, c='b', alpha=0.6, s=0.1)
        plt.plot(time_filtered, temperature_filtered, c='orange', linewidth=0.3, label='Historic data')   
        plt.scatter(t_list2, forecast, c='b', alpha=0.6, s=4)
        plt.plot(t_list2, forecast, c='red', linewidth=0.3, label='Forecasted data')
        plt.scatter(t_list2, forecast2, c='grey', alpha=0.6, s=2)
        plt.plot(t_list2, forecast2, c='grey', linewidth=0.1, label='Forecasted data (bad parameters)')
        plt.scatter(t_list2, forecast3, c='grey', alpha=0.6, s=2)
        plt.plot(t_list2, forecast3, c='grey', linewidth=0.1)
        plt.scatter(t_list2, forecast4, c='grey', alpha=0.6, s=2)
        plt.plot(t_list2, forecast4, c='grey', linewidth=0.1)
        plt.suptitle("Online Machine Learning (forecasting)", fontsize=12)

        plt.ylim(0, 22)

        plt.title("Iteration {y}".format(y=i), fontsize=8)
        plt.legend(loc='lower right')
        plt.savefig("./output_ml/it_{y}.png".format(y=i))
        print("./output_ml/it_{y}.png".format(y=i))
        file_names.append("./output_ml/it_{y}.png".format(y=i))
        plt.close()


import imageio
images = []
for filename in file_names:
    images.append(imageio.imread(filename))
imageio.mimsave('./output_ml/movie_iow.gif', images)
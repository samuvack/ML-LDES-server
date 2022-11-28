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

from sklearn.metrics import r2_score

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
validation_list = []
validation_list2 = []
validation_list3 = []
validation_list4 = []
validation_time=[]
r2_list = []

def mae(y_true, predictions):
    y_true, predictions = np.array(y_true), np.array(predictions)
    return np.mean(np.abs(y_true - predictions))



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
         p=2,
         d=0,
         q=1,
         m=1,
         sp=0,
         sq=0,
         sd=0,
         regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                optimizer=optim.SGD(0.1),
                intercept_lr=0.5
            )
     )
 )
)

model2 = (
time_series.SNARIMAX(
         p=3,
         d=0,
         q=1,
         m=1,
         sp=0,
         sq=0,
         sd=0,
         regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                optimizer=optim.SGD(0.1),
                intercept_lr=0.5
            )
     )
 )
)

model3 = (
time_series.SNARIMAX(
         p=4,
         d=0,
         q=1,
         m=1,
         sp=0,
         sq=0,
         sd=0,
         regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                optimizer=optim.SGD(0.1),
                intercept_lr=0.5
            )
     )
 )
)

model4 = (
time_series.SNARIMAX(
         p=2,
         d=0,
         q=12,
         m=1,
         sp=0,
         sq=0,
         sd=0,
         regressor=(
            preprocessing.StandardScaler() |
            linear_model.LinearRegression(
                optimizer=optim.SGD(0.1),
                intercept_lr=0.5
            )
     )
 )
)

temperature_list = dat['conductivity'].values.tolist()

print(temperature_list)

time_list = dat['id'].values.tolist()
print(time_list)


for i in range(len(dat)):
    print(i)
    print(dat.loc[i, "conductivity"])
    model = model.learn_one(dat.loc[i, "conductivity"])
    model2 = model2.learn_one(dat.loc[i, "conductivity"])
    model3 = model3.learn_one(dat.loc[i, "conductivity"])
    model4 = model4.learn_one(dat.loc[i, "conductivity"])
    
    #Online Forecasting
    forecast = model.forecast(horizon=12)
    forecast2 = model2.forecast(horizon=12)
    forecast3 = model3.forecast(horizon=12)
    forecast4 = model4.forecast(horizon=12)
    print(forecast)

    t_list2=[]
    temperature_filtered = []
    temperature_validation = []
    time_filtered=[]
    for j in range(12):
        t_list2.append(i+j+1)
        temperature_validation.append(temperature_list[i+j+1])

    for t in range(26):
        temperature_filtered.append(temperature_list[i-12+t])
        time_filtered.append(time_list[i-12+t])

    if (i >= 13):
        validation1 = mae(temperature_validation, forecast)
        validation2 = mae(temperature_validation, forecast2)
        validation3 = mae(temperature_validation, forecast3)
        validation4 = mae(temperature_validation, forecast4)

        print(validation1)
        print(validation2)
        print(validation3)
        print(validation4)
        validation_list.append(validation1)
        validation_list2.append(validation2)
        validation_list3.append(validation3)
        validation_list4.append(validation4)
        validation_time.append(i)





        print(temperature_filtered)
        print(time_filtered)
        #Plotting

        fig, axs = plt.subplots(2)
        fig.set_size_inches(30, 10)
        sns.set()
        axs[0].scatter(time_filtered, temperature_filtered, c='black', alpha=0.6, s=4)
        axs[0].plot(time_filtered, temperature_filtered, c='orange', linewidth=1, label='Historic data')

        axs[0].scatter(t_list2, forecast, c='red', alpha=1, s=4)
        axs[0].plot(t_list2, forecast, c='red', linewidth=0.3, label='Forecasted data (SNARIMAX (p=2, q=1, SGD=0.1, intercept_lr=0.5))')

        axs[0].plot(t_list2, forecast2, c='blue', linewidth=0.3, label='Forecasted data (SNARIMAX (p=3, q=1, SGD=0.1, intercept_lr=0.5))')
        axs[0].scatter(t_list2, forecast2, c='b', alpha=0.6, s=4)


        axs[0].plot(t_list2, forecast3, c='black', linewidth=0.3, label='Forecasted data (SNARIMAX (p=4, q=1, SGD=0.1, intercept_lr=0.5))')
        axs[0].scatter(t_list2, forecast3, c='black', alpha=0.6, s=4)

        axs[0].plot(t_list2, forecast4, c='green', linewidth=0.3, label='Forecasted data (SNARIMAX (p=2, q=12, SGD=0.1, intercept_lr=0.5))')
        axs[0].scatter(t_list2, forecast4, c='green', alpha=0.6, s=4)

        #axs[0].plot(t_list2, forecast4, c='black', linewidth=0.3, label='Forecasted data')
        
        #axs[0].suptitle("Online Machine Learning (forecasting)", fontsize=12)

        ymin, ymax = plt.ylim()
        #axs[0].ylim(600, 1000)

        #axs[0].title("Iteration {y} - SNARIMAX model".format(y=i), fontsize=8)
        axs[0].legend(loc='upper left')
        axs[0].set_ylim([600, 1000])
        #axs[0].savefig("./output_ml/it_{y}.png".format(y=i))
        axs[1].plot(validation_time, validation_list, c='red', linewidth=1, label='Mean Absolute Error' )
        axs[1].plot(validation_time, validation_list2, c='blue', linewidth=0.3, label='Mean Absolute Error' )
        axs[1].plot(validation_time, validation_list3, c='black', linewidth=0.3 , label='Mean Absolute Error' )
        axs[1].plot(validation_time, validation_list4, c='green', linewidth=0.3 , label='Mean Absolute Error' )

        axs[1].legend(loc='upper left')
        axs[1].set_ylim([0, 50])

        #plt.show()
        print("./output_ml/it_{y}.png".format(y=i))
        file_names.append("./output_ml/it_{y}.png".format(y=i))
        #plt.suptitle("Real time measured conductivity + forecasting - iteration {y}".format(y=i), fontsize=15)
        axs[0].set_title("Real time measured conductivity + forecasting - iteration {y}".format(y=i), fontsize=15)
        #axs[1].set_title("Cross validation MAE", fontsize=15)

        plt.savefig("./output_ml/it_{y}.png".format(y=i))
        plt.close()


import imageio
images = []
for filename in file_names:
    images.append(imageio.imread(filename))
imageio.mimsave('./output_ml/movie_iow.gif', images)
from river import datasets
from river import metrics
from river import time_series
import datetime as dt
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt


file_names = []

for j in range(143):
    dataset = datasets.AirlinePassengers()

    period = 12
    model = time_series.SNARIMAX(
    p=period,
    d=1,
    q=period,
    m=period,
    sd=1
    )



    horizon=12

    prediction = 0
    forecast = [1]
    
    q=0
    for t, (x, y) in enumerate(datasets.AirlinePassengers()):
        t_list2=[]
        #print('error:', (forecast[0] - prediction))
        model = model.learn_one(float(y))
        print(y)
        forecast = model.forecast(horizon=horizon)
        print(forecast)
        prediction = y
        for i in range(len(forecast)):
            t_list2.append(t+i)

        if (q==j):
            plt.figure()
            sns.set()
            x_list=[]
            y_list=[]
            t_list=[]
            for t, (x, y) in enumerate(datasets.AirlinePassengers()):
                x_list.append(x)
                y_list.append(y)
                t_list.append(t)
            plt.scatter(t_list, y_list, c='r', alpha=0.6, s=4)
            plt.plot(t_list, y_list, linewidth=0.3)
            plt.plot(t_list2, forecast)
            plt.suptitle("Online Machine Learning (forecasting)", fontsize=14)
            plt.title("SNARIMAX - Iteration {y}".format(y=q), fontsize=10)
            plt.savefig("./images/it_{y}.png".format(y=q))
            print("./images/it_{y}.png".format(y=q))
            file_names.append("./images/it_{y}.png".format(y=q))
        q = q+ 1
            
import imageio
images = []
for filename in file_names:
    images.append(imageio.imread(filename))
imageio.mimsave('./images/movie.gif', images)




from river import datasets
from river import metrics
from river import time_series
import datetime as dt

import numpy as np
import matplotlib.pyplot as plt


for j in range(2,143):
    dataset = datasets.AirlinePassengers()

    model = time_series.HoltWinters(
    alpha=0.3,
    beta=0.1,
    gamma=0.6,
    seasonality=12,
    multiplicative=True
    )

    metric = metrics.MAE()

    time_series.evaluate(
    dataset,
    model,
    metric,
    horizon=12
    )

    horizon=12

    prediction = 0
    forecast = [1]
    
    q=0
    for t, (x, y) in enumerate(datasets.AirlinePassengers()):
        t_list2=[]
        print('error:', (forecast[0] - prediction))
        model = model.learn_one(y)
        print(t,x,y)
        forecast = model.forecast(horizon=horizon)
        print(forecast)
        prediction = y
        for i in range(len(forecast)):
            t_list2.append(t+i)

        if (q==j):
            x_list=[]
            y_list=[]
            t_list=[]
            for t, (x, y) in enumerate(datasets.AirlinePassengers()):
                x_list.append(x)
                y_list.append(y)
                t_list.append(t)
            plt.scatter(t_list, y_list, c='r', alpha=0.6, s=2)
            plt.plot(t_list, y_list, linewidth=0.1)
            plt.plot(t_list2, forecast)
            plt.show()
        q = q+ 1
            


"""

    future = [{'month': dt.date(year=1961, month=m, day=1)}
    for m in range(1, horizon + 1)
    ]



    for x, y_pred in zip(future, forecast):
        print(x['month'], f'{y_pred:.3f}')
"""
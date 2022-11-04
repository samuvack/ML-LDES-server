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

    model = time_series.HoltWinters(
    alpha=0.3,
    beta=0.1,
    gamma=0.6,
    seasonality=12,
    multiplicative=True
    )

    """
    alpha: Smoothing parameter for the level.
    beta  (defaults to None): Smoothing parameter for the trend.
    gamma (defaults to None): Smoothing parameter for the seasonality.
    seasonality (defaults to 0): The number of periods in a season.
    multiplicative (defaults to False): Whether or not to use a multiplicative formulation.
    """

    metric = metrics.MAE()

    time_series.evaluate(
    dataset,
    model,
    metric,
    horizon=12
    )

    for t, (x, y) in enumerate(datasets.AirlinePassengers()):
        t_list2=[]
        #print('error:', (forecast[0] - prediction))
        model = model.learn_one(float(y))
        print(y)
        forecast = model.forecast(horizon=12)
        print(forecast)
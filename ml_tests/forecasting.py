import datetime as dt
from river import datasets
from river import time_series
from river import utils

period = 12
model = time_series.SNARIMAX(
p=period,
d=1,
q=period,
m=period,
sd=1
)

for t, (x, y) in enumerate(datasets.AirlinePassengers()):
    model = model.learn_one(y)

horizon = 12



future = [{'month': dt.date(year=1950, month=m, day=1)}
for m in range(1, horizon + 1)
]

forecast = model.forecast(horizon=horizon)
for x, y_pred in zip(future, forecast):
    print(x['month'], f'{y_pred:.3f}')


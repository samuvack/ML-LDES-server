from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas.io.sql as sqlio
from sklearn.metrics import r2_score


def prophet_output(dat)

    dat.drop_duplicates(subset=['ds'])
    m = Prophet()
    m.fit(dat)  # df is a pandas.DataFrame with 'y' and 'ds' columns
    future = m.make_future_dataframe(periods=2)
    print(future.tail())
    m.predict(future)

    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    print(forecast)

    ax = forecast.plot('ds', 'yhat')
    forecast.plot('ds', 'yhat_lower', ax=ax)
    forecast.plot('ds', 'yhat_upper', ax=ax)
    plt.show()




    ax3=m.plot(forecast)
    plt.show()

    ax2 = m.plot_components(forecast)
    plt.show()

